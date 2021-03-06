from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# 1 тест (получение API ключа)
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# 2 тест (получение списка питомцев)
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# 3 тест (добавление питомца)
def test_add_new_pet_with_valid_data(name='Ершик', animal_type='Темный рыцарь',
                                     age='2', pet_photo='images/cat1.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# 4 тест (удаление питомца)
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Ершик', 'Темный рыцарь', '2', 'images/cat1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

# 5 тест (изменение информации о питомце, без фото)
def test_successful_update_self_pet_info(name='Робин', animal_type='Белый рыцарь', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')

# 6 тест (получение API ключа с не верным email)
def test_get_api_key_for_notvalid_user_name(email="123@mail.ru", password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' is not result

# 7 тест (получение API ключа с не верным паролем)
def test_get_api_key_for_notvalid_user_password(email=valid_email, password='12345'):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' is not result

# 8 тест (добавление питомца c некорректными данными (возраст))
def test_add_new_pet_with_notvalid_data(name='Ершик', animal_type='Темный рыцарь',
                                     age='-250', pet_photo='images/cat2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# 9 тест (добавление нового питомца без фото)
def test_add_new_pet_with_nophoto(name='Брюс', animal_type='Вишенка',
                                     age='8'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_nophoto(auth_key, name, animal_type, age)
    assert status == 200

# 10 тест (добавление фото к питомцу)
def test_post_add_foto_to_pet(pet_photo='images/cat2.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception('There is no my pets')

# 11 тест (изменение фото питомца)
def test_post_change_photo_to_pet(pet_photo='images/cat2.jpg')
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
    status, result = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
    value_image1 = result.get('pet_photo')
    _, result2 = pf.add_new_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo='images/cat3.jpg')
    value_image2 = result2.get('pet_photo')
    assert status == 200
    assert value_image1 != value_image2

# 12 тест (добавление нового питомца без фото c не корректным auth_key)
def test_add_new_pet_with_incorrect_key(name='Ирис', animal_type='Цветок',
                                     age='10'):
    auth_key = {'key': 'ea738148a1f19838e1c5d1413877f3691a3731380e733e877b0ae72'}
    status, result = pf.add_new_pet_nophoto(auth_key, name, animal_type, age)
    assert status == 403
    assert 'Forbidden' in result

# 13 тест (добавление нового питомца без фото c не полными данными (возраст))
#def test_add_new_pet_with_incorrect_data(name='Робин-бобин', animal_type='Белый рыцарь'):
#    _, auth_key = pf.get_api_key(valid_email, valid_password)
#    status, result = pf.add_new_pet_nophoto(auth_key, name, animal_type, age)
#    assert status == 400
#тест не работает из за недоделок сайта


# 14 тест (получение списка питомцев c не корректным auth_key )
def test_get_all_pets_with_incorrect_key(filter=''):
    auth_key = {'key': 'ea738148a1f19838e1c5d1413877f3691a3734545e877b0ae72'}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403


# 15 тест (удаление питомца c не корректным auth_key)
def test_successful_delete_self_pet_incorrect_key():
    auth_key = {'key': 'ea738148a1f19838e1c5d1413877f3691a3734545e877b0ae72'}
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Ершик', 'Темный рыцарь', '2', 'images/cat1.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 403
