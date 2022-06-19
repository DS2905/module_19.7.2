from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

# 1 тест (получение API ключа)
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# 2 тест (выпадает список питомцев)
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
#def test_successful_delete_self_pet():
#    _, auth_key = pf.get_api_key(valid_email, valid_password)
#    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

#    if len(my_pets['pets']) == 0:
#        pf.add_new_pet(auth_key, 'Ершик', 'Темный рыцарь', '2', 'images/cat1.jpg')
#        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

#    pet_id = my_pets['pets'][0]['id']
#    status, _ = pf.delete_pet(auth_key, pet_id)

#    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
#    assert status == 200
#    assert pet_id not in my_pets.values()

# 5 тест (изменение информации о питомце)
def test_successful_update_self_pet_info(name='Робин', animal_type='Белый рыцарь', age='5'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception('There is no my pets')

