from deepct_query_reduction import run_deepct_prediction


def test_end_to_end_on_example_01():
    actual = run_deepct_prediction('/deepct-models/deepct-main-01/output/model.ckpt-20000', 'test-data/example-01.jsonl')
    
    assert actual['763'][0] == ("super", 0.2855)
    assert actual['763'][1] == ("rare", 0.15808)
    assert actual['763'][7] == ("movie", 0.82333)
    assert actual['763'][-6] == ("film", 0.81734)
    assert actual['763'][-4] == ("definitely", 0.13306)
    assert len(actual['763']) == 184
    
    assert actual['802'][0] == ("male", 0.13549)
    assert actual['802'][1] == ("little", 0.43677)
    assert actual['802'][7] == ("red", 0.24621)
    assert actual['802'][-3] == ("may", 0.35376)
    assert actual['802'][-2] == ("have", 0.00749)
    assert len(actual['802']) == 215

def test_end_to_end_on_example_02():
    actual = run_deepct_prediction('/deepct-models/deepct-main-01/output/model.ckpt-20000', 'test-data/example-02.jsonl')    

    assert actual['122'][0] == ("little", 0.60008)
    assert actual['122'][1] == ("white", 0.55622)
    assert actual['122'][-2] == ("fox", 0.27084)
    assert actual['122'][-1] == ("5", 0.76575)
    assert len(actual['122']) == 20
    
    assert actual['828'][0] == ("animated", 0.95671)
    assert actual['828'][1] == ("movie", 0.80365)
    assert actual['828'][-4] == ("2009", 0.32082)
    assert actual['828'][-2] == ("2015", 0.28689)
    assert len(actual['828']) == 27