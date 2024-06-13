from load import format_values


def test_format_values_set_empty_values():
    test_data = [{'key_1': 'value1', 'key_2': '', 'key_3': 'value3'}]
    assert format_values(test_data) == [
        {'key_1': 'value1', 'key_2': None, 'key_3': 'value3'}]


def test_format_value_convert_int_string():
    test_data = [{'plant_id': '3.0', 'key_2': 'value2', 'key_3': 'value3'}]
    assert format_values(test_data) == [
        {'plant_id': 3, 'key_2': 'value2', 'key_3': 'value3'}]


def test_format_value_convert_float_string():
    test_data = [{'soil_moisture': '3.03490204923',
                  'key_2': '93.239432', 'temperature': '92.29342423'}]
    assert format_values(test_data) == [{'soil_moisture': 3.03490204923,
                                         'key_2': '93.239432', 'temperature': 92.29342423}]


def test_format_value_correct_scientific_name():
    test_data = [{'scientific_name': '"[Fake sci name]"',
                  'key': 'value'}]
    test_data_other = [{'scientific_name': "'[Fake sci name]'",
                        'key': 'value'}]

    assert format_values(test_data) == [{'scientific_name': 'Fake sci name',
                                         'key': 'value'}]
    assert format_values(test_data_other) == format_values(test_data)


def test_format_value_make_name_upper():
    test_data = [{'name': 'Bird of paradise',
                  'key': 'value'}]

    assert format_values(test_data) == [{'name': 'BIRD OF PARADISE',
                                         'key': 'value'}]
