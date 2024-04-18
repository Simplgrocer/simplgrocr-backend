import datetime
import json
import time
import requests
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from common.utils.env import get_env_vars
from .models import GroceryList
from .serializers import GroceryListSerializer
from rest_framework.response import Response


PDFMONKEY_ENV_VARS = get_env_vars(
    "PDFMONKEY_API_KEY",
    "PDFMONKEY_API_BASE_URL",
    "PDFMONKEY_API_PREFIX",
    "PDFMONKEY_API_VERSION",
    "PDFMONKEY_GROCERY_LIST_SUMMARY_DOCUMENT_TEMPLATE_ID",
)


class GroceryListViewSet(ModelViewSet):
    queryset = GroceryList.objects.all()
    serializer_class = GroceryListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return GroceryList.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=["post"])
    def summary(self, request, pk):
        grocery_list = self.get_object()
        grocery_list_items = grocery_list.items.all()

        grocery_list_dict = {
            "name": grocery_list.name,
            "description": grocery_list.description,
            "total_price": grocery_list.total_price,
            "groceryListItems": [],
        }

        for grocery_list_item in grocery_list_items:
            grocery_list_dict["groceryListItems"].append(
                {
                    "name": grocery_list_item.name,
                    "description": grocery_list_item.description,
                    "rate_measurement_quantity": grocery_list_item.rate_measurement_quantity,
                    "rate_measurement_unit": grocery_list_item.rate_measurement_unit,
                    "rate": grocery_list_item.rate,
                    "quantity_measurement_unit": grocery_list_item.quantity_measurement_unit,
                    "quantity": grocery_list_item.quantity,
                    "price": grocery_list_item.price,
                }
            )

        document_file_name = f"{grocery_list.name}-{datetime.datetime.now()}.pdf"

        document_generation_scheduler_api_headers = {
            "Authorization": f"Bearer {PDFMONKEY_ENV_VARS['PDFMONKEY_API_KEY']}",
            "Content-Type": "application/json",
        }

        document_generation_scheduler_api_payload = json.dumps(
            {
                "document": {
                    "document_template_id": PDFMONKEY_ENV_VARS[
                        "PDFMONKEY_GROCERY_LIST_SUMMARY_DOCUMENT_TEMPLATE_ID"
                    ],
                    "payload": grocery_list_dict,
                    "status": "pending",
                    "meta": {"_filename": document_file_name},
                }
            }
        )

        try:
            document_generation_scheduler_api_response = requests.request(
                "POST",
                f"{PDFMONKEY_ENV_VARS['PDFMONKEY_API_BASE_URL']}/{PDFMONKEY_ENV_VARS['PDFMONKEY_API_PREFIX']}/{PDFMONKEY_ENV_VARS['PDFMONKEY_API_VERSION']}/documents",
                headers=document_generation_scheduler_api_headers,
                data=document_generation_scheduler_api_payload
            )
        except requests.exceptions.HTTPError as http_err:
            return Response({"detail": "Internal Server Error"}, status=500)
        
        except requests.exceptions.ConnectionError as conn_err:
            return Response({"detail": "Internal Server Error"}, status=500)
            
        except requests.exceptions.Timeout as timeout_err:
            return Response({"detail": "Internal Server Error"}, status=500)
        
        except requests.exceptions.RequestException as err:
            return Response({"detail": "Internal Server Error"}, status=500)
        
        if not document_generation_scheduler_api_response.status_code == 201:
            return Response({"detail": "Internal Server Error"}, status=500)

        try:
            document_generation_scheduler_api_response_json = document_generation_scheduler_api_response.json()
        except requests.exceptions.JSONDecodeError:
            return Response({"detail": "Internal Server Error"}, status=500)
        
        try:
            document_id = document_generation_scheduler_api_response_json["document"]["id"]
        except KeyError:
            return Response({"detail": "Internal Server Error"}, status=500)
        
        time_elapsed = 1

        while time_elapsed < 5:
            try:
                document_generation_document_getter_api_response = requests.request(
                    "GET",
                    f"{PDFMONKEY_ENV_VARS['PDFMONKEY_API_BASE_URL']}/{PDFMONKEY_ENV_VARS['PDFMONKEY_API_PREFIX']}/{PDFMONKEY_ENV_VARS['PDFMONKEY_API_VERSION']}/document_cards/{document_id}",
                    headers=document_generation_scheduler_api_headers
                )
            except requests.exceptions.HTTPError as http_err:
                return Response({"detail": "Internal Server Error"}, status=500)

            except requests.exceptions.ConnectionError as conn_err:
                return Response({"detail": "Internal Server Error"}, status=500)
                
            except requests.exceptions.Timeout as timeout_err:
                return Response({"detail": "Internal Server Error"}, status=500)

            except requests.exceptions.RequestException as err:
                return Response({"detail": "Internal Server Error"}, status=500)

            if not document_generation_document_getter_api_response.status_code == 200:
                return Response({"detail": "Internal Server Error"}, status=500)
            
            try:
                document_generation_document_getter_api_response_json = document_generation_document_getter_api_response.json()
            except requests.exceptions.JSONDecodeError:
                return Response({"detail": "Internal Server Error"}, status=500)

            try:
                download_url = document_generation_document_getter_api_response_json["document_card"]["download_url"]
            except KeyError:
                return Response({"detail": "Internal Server Error"}, status=500)
            
            if download_url is None:
                time.sleep(1)

                time_elapsed += 1

                continue

            return Response({"download_url": download_url}, status=200)
