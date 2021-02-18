def test_get_condition_new():
  scraper = Scraper('Apple', 3000, 'new')
  result = scraper.condition_code

  assert result == 1000

def test_get_condition_used():
  scraper = Scraper('Apple', 3000, 'used')
  result = scraper.condition_code

  assert result == 3000

def test_get_condition_error():
  scraper = Scraper('Apple', 3000, 'something else')
  with pytest.raises(KeyError):
    scraper.condition_code

def test_get_brand_id_apple():
  scraper = Scraper('Apple', 3000, 'used')
  result = scraper.brand_id

  assert result == 319682

def test_get_brand_id_lg():
  scraper = Scraper('LG', 3000, 'used')
  result = scraper.brand_id

  assert result == 353985

def test_get_brand_id_huawei():
  scraper = Scraper('Huawei', 3000, 'used')
  result = scraper.brand_id

  assert result == 349965

def test_get_brand_id_samsung():
  scraper = Scraper('Samsung', 3000, 'used')
  result = scraper.brand_id

  assert result == 352130

def test_get_brand_id_error():
  scraper = Scraper('Something else', 3000, 'new')
  with pytest.raises(KeyError):
    scraper.brand_id

def test_get_num_of_pages_true():
  scraper = Scraper('Apple', 48, 'new')
  result = scraper.num_of_pages

  assert result == 1

def test_get_num_of_pages_error():
  scraper = Scraper('Something else', '3000', 'new')
  with pytest.raises(TypeError):
    scraper.num_of_pages