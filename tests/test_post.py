import pytest
import allure


@allure.feature('Publication Creation')
@allure.story('Create New Publication')
@pytest.mark.smoke
def test_create_post_not_complete_payload(token, create_post):
    payload = {
        "text": "Git mosquitoess"
    }
    create_post.create_new_publication(token=token, payload=payload)
    create_post.check_response_is_400()


@allure.feature('Publication Creation')
@allure.story('Create New Publication')
@pytest.mark.smoke
def test_create_post(token, create_post):
    payload = {
        "text": "Git mosquitoess",
        "url": "https://9gag.com/gag/amoNKdV",
        "tags": ["mosquito", "spray"],
        "info": {"colors": ["red", "white"], "objects": ["picture", "text"]},
    }
    create_post.create_new_publication(token=token, payload=payload)
    create_post.check_response_is_200()


@allure.feature('Security')
@allure.story('Unauthorized Access')
@pytest.mark.security
def test_access_without_token(create_post):
    payload = {
        "text": "Git mosquitoess",
        "url": "https://9gag.com/gag/amoNKdV",
        "tags": ["mosquito", "spray"],
        "info": {"colors": ["red", "white"], "objects": ["picture", "text"]},
    }

    create_post.create_new_publication(token=None, payload=payload)
    create_post.check_response_is_401()


@allure.feature('Publication Validation')
@allure.story('Invalid Data Handling')
@pytest.mark.parametrize('text_input', [123, {"key": "value"}, [], (1,)], ids=['int', 'dict', 'list', 'tuple'])
@pytest.mark.functional
def test_create_post_invalid_text(text_input, token, create_post):
    payload = {
        "text": text_input,
        "url": "https://9gag.com/gag/amoNKdV",
        "tags": ["test", "example"],
        "info": {"colors": ["blue"], "objects": ["lamp"]}
    }
    create_post.create_new_publication(token=token, payload=payload)
    create_post.check_response_is_400()


@allure.feature('Publication Data Validation')
@allure.story('Tags Data Type Validation')
@pytest.mark.parametrize('tags_input', [123, {"key": "value"}, "string", True, None],
                         ids=['integer', 'dictionary', 'string', 'Boolean', 'None'])
@pytest.mark.functional
def test_create_post_invalid_tags(token, tags_input, create_post):
    payload = {
        "text": "Sample text for validation",
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": tags_input,
        "info": {"colors": ["blue"], "objects": ["book"]}
    }
    create_post.create_new_publication(token=token, payload=payload)
    create_post.check_response_is_400()


@allure.feature('Publication Data Validation')
@allure.story('Info Field Data Type Validation')
@pytest.mark.parametrize('info_input, expected_status', [({"colors": ["blue"], "objects": ["book"]}, 200),
                                                         (123, 400), (["not", "a", "dictionary"], 400),
                                                         ("string", 400), (True, 400), (False, 400),
                                                         (None, 400)],
                         ids=['valid_dict', 'integer', 'list', 'string', 'true_boolean', 'false_boolean', 'none'])
@pytest.mark.functional
def test_create_post_invalid_info(token, info_input, expected_status, create_post):
    payload = {
        "text": "Sample text for validation",
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": ["valid", "tags"],
        "info": info_input
    }
    create_post.create_new_publication(token=token, payload=payload)
    create_post.check_expected_status(create_post.response, expected_status)


@allure.feature('Meme Retrieval')
@allure.story('Check Meme ID and Response Status')
@pytest.mark.smoke
def test_get_id_post(token, meme_id, get_id_post):
    get_id_post.get_id_publication(token=token, meme_id=meme_id)
    get_id_post.check_response_is_200()
    get_id_post.check_id_is_correct(meme_id=meme_id)


@allure.feature('Meme Retrieval')
@allure.story('Check Nonexistent Meme ID')
@pytest.mark.functional
def test_get_nonexistent_id(token, meme_id, get_id_post):
    get_id_post.get_id_publication(token=token, meme_id=None)
    get_id_post.check_response_is_404()


@allure.feature('Meme Retrieval')
@allure.story('Check Unauthorized Access Without Token')
@pytest.mark.security
def test_get_request_without_token(meme_id, get_id_post):
    get_id_post.get_id_publication(None, meme_id=meme_id)
    get_id_post.check_response_is_401()


@allure.feature('Meme Retrieval')
@allure.story('Check Response for Nonexistent String Meme ID')
@pytest.mark.functional
def test_get_nonexistent_string_id(token, get_id_post, meme_id):
    nonexistent_id = 'invalid_string_id'
    get_id_post.get_id_publication(token=token, meme_id=nonexistent_id)
    get_id_post.check_response_is_404()


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.functional
def test_put_post(token, meme_id, put_post):
    payload = {
        "id": meme_id,
        "text": "Loll",
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": ["senior", "girls"],
        "info": {"cloth": ["trousers", "t-shirt"], "objects": ["picture", "text"]},
    }
    put_post.put_new_publication(token=token, meme_id=meme_id, payload=payload)
    put_post.check_response_is_200()
    put_post.check_text(text=payload['text'])


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.parametrize("input_text, expected_status_code",
                         [("Valid Text", 200), (12345, 400),
                          ("", 200), ("very long text " + "a" * 10000, 200),
                          (None, 400)])
def test_invalid_data_type(token, meme_id, input_text, expected_status_code, put_post):
    payload = {
        "id": meme_id,
        "text": input_text,
        "url": "https://9gag.com/gag/aQzPBmW",
        "tags": ["senior", "girls"],
        "info": {"cloth": ["trousers", "t-shirt"], "objects": ["picture", "text"]}
    }
    put_post.put_new_publication(token=token, meme_id=meme_id, payload=payload)
    put_post.check_expected_status(put_post.response, expected_status_code)


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.functional
def test_empty_update_body(token, meme_id, put_post):
    payload = {}
    put_post.put_new_publication(token=token, meme_id=meme_id, payload=payload)
    put_post.check_response_is_400()


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.security
def test_unauthorized_request(token, meme_id, put_post):
    payload = {
        "id": meme_id,
        "text": "Unauthorized attempt"
    }

    put_post.put_new_publication(token=None, meme_id=meme_id, payload=payload)
    put_post.check_response_is_401()


@allure.feature('Meme Modification')
@allure.story('Update Meme Information')
@pytest.mark.functional
def test_update_single_field(token, meme_id, put_post):
    payload = {
        "id": meme_id,
        "text": "Updated text only"
    }
    put_post.put_new_publication(token=None, meme_id=meme_id, payload=payload)
    put_post.check_response_is_401()


@allure.feature('Meme Deletion')
@allure.story('Delete Meme and Verify Deletion')
@pytest.mark.functional
def test_delete_post(token, meme_id, delete_post, get_id_post):
    delete_post.delete_publication(token=token, meme_id=meme_id)
    delete_post.check_response_is_200()
    get_id_post.get_id_publication(token=token, meme_id=meme_id)
    get_id_post.check_response_is_404()


@allure.feature('Meme Deletion')
@allure.story('Attempt to Delete with Invalid Token')
@pytest.mark.security
def test_delete_with_invalid_token(meme_id, token, delete_post):
    invalid_token = "some_invalid_token"
    delete_post.delete_publication(token=invalid_token, meme_id=meme_id)
    delete_post.check_response_is_401()


@allure.feature('Meme Deletion')
@allure.story('Delete Nonexistent Meme')
@pytest.mark.negative
def test_delete_nonexistent_meme(token, delete_post):
    nonexistent_id = "nonexistent_id"
    delete_post.delete_publication(token=token, meme_id=nonexistent_id)
    delete_post.check_response_is_404()


@allure.feature('Meme Deletion')
@allure.story('Delete Meme Without ID')
@pytest.mark.negative
def test_delete_without_id(token, delete_post):
    delete_post.delete_publication(token=token, meme_id=None)
    delete_post.check_response_is_404()
