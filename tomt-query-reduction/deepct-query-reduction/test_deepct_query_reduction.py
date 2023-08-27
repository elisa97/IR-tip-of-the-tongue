from deepct_query_reduction import DeepCTQueryReduction, determine_per_query_threshold

def test_query_reduction_01():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-0;None')
    
    actual = query_reduction.reduce_query('763')
    assert actual.startswith('super rare surreal dystopian masterpiece very rare movie that is scifi dystopian experimental surreal it like stalker meets el topo meets holy mountain meets alphaville meets delicatessen meets hard to')
    assert 145 == len(actual.split())
    assert actual.endswith('actually rare movies this film is definitely not')

def test_query_reduction_02():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-0;None')
    
    actual = query_reduction.reduce_query({'qid': '763', 'query': 'x y z'})
    assert actual.startswith('super rare surreal dystopian masterpiece very rare movie that is scifi dystopian experimental surreal it like stalker meets el topo meets holy mountain meets alphaville meets delicatessen meets hard to')
    assert 145 == len(actual.split())
    assert actual.endswith('actually rare movies this film is definitely not')

def test_query_reduction_03():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-22503;None')
    
    actual = query_reduction.reduce_query({'qid': '802', 'query': 'x y z'})
    assert actual.startswith('male little person falls in love with red headed woman hope someone can help me track down this movie')
    assert 180 == len(actual.split())
    assert actual.endswith('thank you in advance for any suggestions you may have')


def test_query_reduction_04():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-0;1.0')
    
    actual = query_reduction.reduce_query('763')
    assert actual.startswith('super rare surreal dystopian masterpiece very rare movie that is scifi dystopian experimental surreal it like stalker meets el topo meets holy mountain meets alphaville meets delicatessen meets hard to')
    assert 145 == len(actual.split())
    assert actual.endswith('actually rare movies this film is definitely not')

def test_query_reduction_05():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-0;1.0')
    
    actual = query_reduction.reduce_query({'qid': '763', 'query': 'x y z'})
    assert actual.startswith('super rare surreal dystopian masterpiece very rare movie that is scifi dystopian experimental surreal it like stalker meets el topo meets holy mountain meets alphaville meets delicatessen meets hard to')
    assert 145 == len(actual.split())
    assert actual.endswith('actually rare movies this film is definitely not')

def test_query_reduction_06():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-22503;1.0')
    
    actual = query_reduction.reduce_query({'qid': '802', 'query': 'x y z'})
    assert actual.startswith('male little person falls in love with red headed woman hope someone can help me track down this movie')
    assert 180 == len(actual.split())
    assert actual.endswith('thank you in advance for any suggestions you may have')

def test_query_reduction_07():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-22503;0.5')
    
    actual = query_reduction.reduce_query({'qid': '802', 'query': 'x y z'})
    assert 90 == len(actual.split())
    assert actual.startswith('male little person falls love red headed woman hope someone help track movie may details')
   
    assert actual.endswith('fetched please share thank you advance for suggestions you may')

def test_query_reduction_08():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-22503;0.25')
    
    actual = query_reduction.reduce_query({'qid': '802', 'query': 'x y z'})
    assert 45 == len(actual.split())
    assert actual.startswith('little person falls love headed woman help track movie may details mixed another drama suggestions')
   
    assert actual.endswith('last scene movie dancing white wedding people actors failed please share thank suggestions may')


def test_query_reduction_09():
    query_reduction = DeepCTQueryReduction('tot-train-deepct-predictions/predictions.json', '/deepct-models/deepct-main-01/output/model.ckpt-22503;0.1')
    
    actual = query_reduction.reduce_query({'qid': '802', 'query': 'x y z'})
    assert 18 == len(actual.split())
    assert actual.startswith('person love headed help movie details drama man person working life life writer plot making people')
   
    assert actual.endswith('life writer plot making people last movie')

def test_determine_per_query_threshold_01():
    input = [['T1', 0.1], ['T2', 0.2], ['T3', 0.3], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6]]
    expected = 0.1
    actual = determine_per_query_threshold(input, 1.0)

    assert expected == actual

def test_determine_per_query_threshold_02():
    input = [['T1', 0.1], ['T2', 0.2], ['T3', 0.3], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6]]
    expected = -1000000
    actual = determine_per_query_threshold(input, None)

    assert expected == actual

def test_determine_per_query_threshold_03():
    input = [['T1', 0.1], ['T2', 0.2], ['T3', 0.3], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6]]
    expected = 0.1
    actual = determine_per_query_threshold(input, 0.9)

    assert expected == actual

def test_determine_per_query_threshold_04():
    input = [['T1', 0.1], ['T2', 0.2], ['T3', 0.3], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6]]
    expected = 0.2
    actual = determine_per_query_threshold(input, 0.8)

    assert expected == actual

def test_determine_per_query_threshold_05():
    input = [['T1', 0.1], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6], ['T2', 0.2], ['T3', 0.3],]
    expected = 0.2
    actual = determine_per_query_threshold(input, 0.8)

    assert expected == actual

def test_determine_per_query_threshold_06():
    input = [['T1', 0.1], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6], ['T2', 0.2], ['T3', 0.3],]
    expected = 0.1
    actual = determine_per_query_threshold(input, 0.9)

    assert expected == actual

def test_determine_per_query_threshold_07():
    input = [['T1', 0.1], ['T4', 0.4], ['T5', 0.5], ['T6', 0.6], ['T2', 0.2], ['T3', 0.3],]
    expected = 0.4
    actual = determine_per_query_threshold(input, 0.5)

    assert expected == actual