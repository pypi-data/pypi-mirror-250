
Translator ARS Pass/Fail Testing 
==========================================================

This testing framework performs single level pass/Fail analysis on queries it receives from the Test Runner. 

### ARS_Test Implementation
```bash
pip install ARS_Test_Runner 
```

### CLI
The command-line interface is the easiest way to run the ARS_Test_Runner
After installation, simply type ARS_Test_Runner --help to see required input arguments & options
- `ARS_Test_Runner`
    - env : the environment to run the queries against (dev|ci|test|prod)
    - predicate: treats
    - runner_setting: creative mode inidicator (inferred)
    - expected_output: TopAnswer|Acceptable|BadButForgivable|NeverShow
    - input_curie: normalized curie taken from assest.csv
    - output_curie: target output curie to do analysis on

- example:
  - for single output
    - ARS_Test_Runner --env 'test' --predicate 'treats' --runner_setting '["inferred"]'  --expected_output '["TopAnswer"]' --input_curie 'MONDO:0015564' --output_curie '["PUBCHEM.COMPOUND:5284616"]'
  - for multi outputs
    - ARS_Test_Runner --env 'ci' --predicate 'treats' --runner_setting '["inferred"]' --expected_output '["TopAnswer","TopAnswer"]' --input_curie 'MONDO:0005301' --output_curie '["PUBCHEM.COMPOUND:107970","UNII:3JB47N2Q2P"]'


### python
``` python 
import asyncio
from ARS_Test_Runner.semantic_test import run_semantic_test
asyncio.run(run_semantic_test('ci','treats',['inferred'], ['TopAnswer','TopAnswer'],'MONDO:0005301',['PUBCHEM.COMPOUND:107970','UNII:3JB47N2Q2P']))
```
OR
``` python 
python semantic_test.py --env 'ci' --predicate 'treats' --runner_setting 'inferred'  --expected_output 'TopAnswer' 'TopAnswer' --input_curie 'MONDO:0005301' --output_curie 'PUBCHEM.COMPOUND:107970' 'UNI:3JB47N2Q2P'
```






