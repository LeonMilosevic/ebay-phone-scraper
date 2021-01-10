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

def calculate_number_of_pages():
    result = scraper.calculate_number_of_pages(48)

    assert result == 1

# needs updating
def get_phones_url():
    result = scraper.get_phones_url(
        number_of_pages=1,
        brand="Apple",
        brandId=319682,
        user_agent=UserAgent()
    )

    assert result == list
