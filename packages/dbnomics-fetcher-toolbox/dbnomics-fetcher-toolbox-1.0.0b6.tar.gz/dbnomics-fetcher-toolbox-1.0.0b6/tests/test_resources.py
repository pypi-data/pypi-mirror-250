import pytest


@pytest.mark.parametrize("resource_id", ["a", "foo"])
def test_check_resource_id__valid(resource_id: ResourceId) -> None:
    check_resource_id(resource_id)


@pytest.mark.parametrize("resource_id", ["", " ", "a b", "a,b", "a/b"])
def test_check_resource_id__invalid(resource_id: ResourceId) -> None:
    with pytest.raises(InvalidResourceId):
        check_resource_id(resource_id)
