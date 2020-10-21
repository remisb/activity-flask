from activity.service.vote_rate import VoteRate
import logging

expected_rates = {1: 1.0, 2: 0.5, 3: 0.25, 4: 0.25}


def assert_vote_rate(vr: float, call):
    logging.getLogger().info(
        f'vr: {vr} call: {call} expect:{expected_rates[call]}')
    assert vr == expected_rates[call]


def test_vote_rates():
    vr = VoteRate()
    vr1_1 = vr.next_rate(1)
    assert_vote_rate(vr1_1, 1)
    vr1_2 = vr.next_rate(1)
    assert_vote_rate(vr1_2, 2)
    vr1_3 = vr.next_rate(1)
    assert_vote_rate(vr1_3, 3)
    vr1_4 = vr.next_rate(1)
    assert_vote_rate(vr1_4, 4)

    vr2_1 = vr.next_rate(2)
    assert_vote_rate(vr2_1, 1)
    vr2_2 = vr.next_rate(2)
    assert_vote_rate(vr2_2, 2)
