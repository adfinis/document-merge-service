import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "query_params,expected",
    [
        ({"page_size": 10}, 10),
        ({"page_size": 120}, 110),  # max page size reached
        ({}, 100),  # default page size
    ],
)
def test_pagination(db, client, template_factory, query_params, expected, mocker):
    mocker.patch(
        "document_merge_service.api.pagination.APIPagination.max_page_size", 110
    )

    template_factory.create_batch(120)

    response = client.get(reverse("template-list"), data=query_params)

    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert result["count"] == 120
    assert len(result["results"]) == expected
