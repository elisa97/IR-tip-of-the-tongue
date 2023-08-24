from deepct_query_reduction import parse_deepct_output

def test_parsing_of_output_from_deepct_01():
    input = '''the 0.00649     presence 0.32891        of 0.00544      communication 0.82666   amid 0.11675    scientific 0.83544      minds 0.66246   was 0.00797     equally 0.23293      important 0.61936       to 0.00985      the 0.00771     success 0.68445 of 0.00871      the 0.01521     manhattan 0.84130       project 0.97619 as 0.01184  scientific 0.83459       intellect 0.30922       was 0.00327     . 0.00849       the 0.00454     only 0.01046    cloud 0.19257   hanging 0.14064 over 0.00704    the 0.00567  impressive 0.38083      achievement 0.52639     of 0.00781      the 0.00938     atomic 0.75888  researchers 0.72138     and 0.01411     engineers 0.77066   is 0.00816       what 0.01076    their 0.00464   success 0.68402 truly 0.24912   meant 0.23745   ; 0.01055       hundreds 0.49705        of 0.00744      thousands 0.63341    of 0.00770      innocent 0.18881        lives 0.77584   ob 0.11131      ##lite 0.00000  ##rated 0.00000 . 0.01174       [SEP] 0.00000'''
    actual = parse_deepct_output(input)[0]

    assert actual[0] == ('the', 0.00649)
    assert actual[3] == ('communication', 0.82666)
    assert actual[4] == ('amid', 0.11675)
    assert actual[9] == ('important', 0.61936)
    assert actual[19] == ('intellect', 0.30922)
    assert actual[48] == ('lives', 0.77584)
    assert actual[49] == ('obliterated', 0.11131)
    assert actual[50] == ('.', 0.01174)
    assert len(actual) == 51


def test_parsing_of_output_from_deepct_02():
    input = '''a 0.00649     ##b 0.000032891        ##c 0.0000544      ##d 0.000082666   ##e 0.000011675    is 0.83544      ##a 0.66246   ##b 0.00797     ##c 0.23293 '''
    actual = parse_deepct_output(input)[0]

    assert actual[0] == ('abcde', 0.00649)
    assert actual[1] == ('isabc', 0.83544)
    assert len(actual) == 2

def test_term_has_max_token_score():
    input = '''a 0.00649     ##b 0.32891        ##c 0.00544      ##d 0.82666   ##e 0.11675    is 0.83544      ##a 0.66246   ##b 0.00797     ##c 0.23293 '''
    actual = parse_deepct_output(input)[0]

    assert actual[0] == ('abcde', 0.82666)
    assert actual[1] == ('isabc', 0.83544)
    assert len(actual) == 2