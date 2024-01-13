from omymodels import create_models


ddl = """
CREATE TABLE `option` (
  `opt_id` int(10) UNSIGNED NOT NULL,
) CHARSET=utf8;

ALTER TABLE `option`
  ADD PRIMARY KEY (`opt_id`);
"""
result = create_models(ddl, models_type='pydantic', no_auto_snake_case=True)['code']
print(result)