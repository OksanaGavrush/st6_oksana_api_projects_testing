from copy import deepcopy
import pytest
import allure
from tests.data import default_payload


@allure.feature('Publication Creation')
@allure.story('Create New Publication')
@pytest.mark.smoke
def test_create_meme_not_complete_payload(token, make_post):
    payload = {
        "text": "Git mosquitoess"
    }
    make_post.create_new_meme(token=token, payload=payload)
    make_post.check_response_is_400()


@allure.feature('Publication Creation')
@allure.story('Create New Publication')
@pytest.mark.smoke
def test_create_meme(token, make_post):
    payload = deepcopy(default_payload)
    make_post.create_new_meme(token=token, payload=payload)
    make_post.check_response_is_200()


@allure.feature('Security')
@allure.story('Unauthorized Access')
@pytest.mark.security
def test_access_without_token(make_post):
    payload = deepcopy(default_payload)
    make_post.create_new_meme(token=None, payload=payload)
    make_post.check_response_is_401()


@allure.feature('Publication Validation')
@allure.story('Invalid Data Handling')
@pytest.mark.parametrize('text_input', [123, {"key": "value"}, [], (1,)], ids=['int', 'dict', 'list', 'tuple'])
@pytest.mark.functional
def test_create_meme_invalid_text(text_input, token, make_post):
    payload = deepcopy(default_payload)
    payload['text'] = text_input
    make_post.create_new_meme(token=token, payload=payload)
    make_post.check_response_is_400()


@allure.feature('Publication Data Validation')
@allure.story('Tags Data Type Validation')
@pytest.mark.parametrize('tags_input', [123, {"key": "value"}, "string", True, None],
                         ids=['integer', 'dictionary', 'string', 'Boolean', 'None'])
@pytest.mark.functional
def test_create_meme_invalid_tags(token, tags_input, make_post):
    payload = deepcopy(default_payload)
    payload["tags"] = tags_input
    make_post.create_new_meme(token=token, payload=payload)
    make_post.check_response_is_400()


@allure.feature('Publication Data Validation')
@allure.story('Info Field Data Type Validation')
@pytest.mark.parametrize('info_input, expected_status', [({"colors": ["blue"], "objects": ["book"]}, 200),
                                                         (123, 400), (["not", "a", "dictionary"], 400),
                                                         ("string", 400), (True, 400), (False, 400),
                                                         (None, 400)],
                         ids=['valid_dict', 'integer', 'list', 'string', 'true_boolean', 'false_boolean', 'none'])
@pytest.mark.functional
def test_create_meme_invalid_info(token, info_input, expected_status, make_post):
    payload = {
        "text": "Sample text for validation",
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": ["valid", "tags"],
        "info": info_input
    }
    make_post.create_new_meme(token=token, payload=payload)
    make_post.check_expected_status(make_post.response, expected_status)


@allure.feature('Meme Retrieval')
@allure.story('Check Meme ID and Response Status')
@pytest.mark.smoke
def test_get_id_meme(token, meme_id, get_id_meme):
    get_id_meme.retrieve_meme(token=token, meme_id=meme_id)
    get_id_meme.check_response_is_200()
    get_id_meme.check_id_is_correct(meme_id=meme_id)


@allure.feature('Meme Retrieval')
@allure.story('Check Nonexistent Meme ID')
@pytest.mark.functional
def test_get_nonexistent_id(token, meme_id, get_id_meme):
    get_id_meme.retrieve_meme(token=token, meme_id=None)
    get_id_meme.check_response_is_404()


@allure.feature('Meme Retrieval')
@allure.story('Check Unauthorized Access Without Token')
@pytest.mark.security
def test_get_request_without_token(meme_id, get_id_meme):
    get_id_meme.retrieve_meme(None, meme_id=meme_id)
    get_id_meme.check_response_is_401()


@allure.feature('Meme Retrieval')
@allure.story('Check Response for Nonexistent String Meme ID')
@pytest.mark.functional
def test_get_nonexistent_string_id(token, get_id_meme, meme_id):
    nonexistent_id = 'invalid_string_id'
    get_id_meme.retrieve_meme(token=token, meme_id=nonexistent_id)
    get_id_meme.check_response_is_404()


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.functional
def test_put_meme(token, meme_id, put_meme):
    payload = {
        "id": meme_id,
        "text": "Loll",
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": ["senior", "girls"],
        "info": {"cloth": ["trousers", "t-shirt"], "objects": ["picture", "text"]},
    }
    put_meme.put_new_meme(token=token, meme_id=meme_id, payload=payload)
    put_meme.check_response_is_200()
    put_meme.check_text(text=payload['text'])


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.parametrize("input_text, expected_status_code",
                         [("Valid Text", 200), (12345, 400),
                          ("", 200), ("very long text " + "a" * 10000, 200),
                          (None, 400)])
def test_invalid_data_type(token, meme_id, input_text, expected_status_code, put_meme):
    payload = {
        "id": meme_id,
        "text": input_text,
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": ["senior", "girls"],
        "info": {"cloth": ["trousers", "t-shirt"], "objects": ["picture", "text"]}
    }
    put_meme.put_new_meme(token=token, meme_id=meme_id, payload=payload)
    put_meme.check_expected_status(put_meme.response, expected_status_code)


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.functional
def test_empty_update_body(token, meme_id, put_meme):
    payload = {}
    put_meme.put_new_meme(token=token, meme_id=meme_id, payload=payload)
    put_meme.check_response_is_400()


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.security
def test_unauthorized_request(token, meme_id, put_meme):
    payload = {
        "id": meme_id,
        "text": "Unauthorized attempt"
    }

    put_meme.put_new_meme(token=None, meme_id=meme_id, payload=payload)
    put_meme.check_response_is_401()


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.functional
def test_update_single_field(token, meme_id, put_meme):
    payload = {
        "id": meme_id,
        "text": "Updated text only"
    }
    put_meme.put_new_meme(token=None, meme_id=meme_id, payload=payload)
    put_meme.check_response_is_401()


@allure.feature('Meme Deletion')
@allure.story('Delete Meme and Verify Deletion')
@pytest.mark.functional
def test_delete_meme(token, meme_id, remove_post, get_id_meme):
    remove_post.remove_meme(token=token, meme_id=meme_id)
    remove_post.check_response_is_200()
    get_id_meme.retrieve_meme(token=token, meme_id=meme_id)
    get_id_meme.check_response_is_404()


@allure.feature('Meme Deletion')
@allure.story('Attempt to Delete with Invalid Token')
@pytest.mark.security
def test_delete_with_invalid_token(meme_id, token, remove_post):
    invalid_token = "some_invalid_token"
    remove_post.remove_meme(token=invalid_token, meme_id=meme_id)
    remove_post.check_response_is_401()


@allure.feature('Meme Deletion')
@allure.story('Delete Nonexistent Meme')
@pytest.mark.negative
def test_delete_nonexistent_meme(token, remove_post):
    nonexistent_id = "nonexistent_id"
    remove_post.remove_meme(token=token, meme_id=nonexistent_id)
    remove_post.check_response_is_404()


@allure.feature('Meme Deletion')
@allure.story('Delete Meme Without ID')
@pytest.mark.negative
def test_delete_without_id(token, remove_post):
    remove_post.remove_meme(token=token, meme_id=None)
    remove_post.check_response_is_404()
