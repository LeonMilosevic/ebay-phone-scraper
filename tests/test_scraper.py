def test_check_brandIdApple():
  result = scraper.check_brandId('Apple')

  assert result == 319682

def test_check_brandIdLG():
  result = scraper.check_brandId('LG')

  assert result == 353985

def test_check_brandIdHuawei():
  result = scraper.check_brandId('Huawei')

  assert result == 349965

def test_check_brandIdSamsung():
  result = scraper.check_brandId('Samsung')

  assert result == 352130

def test_check_brandIdError():
  with pytest.raises(ValueError):
      scraper.check_brandId('bad')

def test_check_conditionNew():
  result = scraper.check_condition('new')

  assert result == 1000

def test_check_conditionUsed():
  result = scraper.check_condition('used')

  assert result = 3000

def test_check_conditionError():
    with pytest.raises(ValueError):
        scraper.check_condition('something else')

def test_calculate_number_of_pages():
    result = scraper.calculate_number_of_pages(48)

    assert result == 1

def test_get_phones_url():
    result = scraper.get_phones_url(
        number_of_pages=1,
        brand="Apple",
        brandId=319682,
        user_agent=UserAgent()
    )

    assert len(result) == 42

def test_create_datafrmae():
  brand = "Apple"
  phone_price = ['123', '456', '789']
  phone_model = ['galaxy', 'iphone 7', 'iphone 8']
  phone_ram = ['3 gb', '4gb', '5gb']
  phone_storage = ['64gb', '128gb', '16gb']
  phone_processor = ['some processor', 'some processor2', 'some processor3']
  phone_camera = ['16', '8', '12']

  result = scraper.create_datafrmae(
    brand, 
    phone_price, 
    phone_model, 
    phone_ram, 
    phone_storage, 
    phone_processor, 
    phone_camera)

    assert type(result) == pd.DataFrame