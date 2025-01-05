from randomness_testsuite import FrequencyTest, RunTest, Spectral, TemplateMatching, Universal, Complexity, Serial, ApproximateEntropy, CumulativeSum, RandomExcursions
import sys
from collections import Counter

def to_bin(data):
    if type(data) == str:
        data = data.encode()
        return bin(int.from_bytes(data, byteorder=sys.byteorder))[2:]
    elif type(data) in [bytes, bytearray]:
        return bin(int.from_bytes(data, byteorder=sys.byteorder))[2:]
    else:
        raise TypeError

def nist_tests(data) -> bool:
    d = to_bin(data)

    freq = FrequencyTest.FrequencyTest()
    runs = RunTest.RunTest()
    fft = Spectral.SpectralTest()
    matcher = TemplateMatching.TemplateMatching()
    maurer = Universal.Universal()
    linear_c = Complexity.ComplexityTest()
    serial = Serial.Serial()
    entropy = ApproximateEntropy.ApproximateEntropy()
    cusum = CumulativeSum.CumulativeSums()
    exc = RandomExcursions.RandomExcursions()

    try:
        _, monobit_verdict = freq.monobit_test(d)
        _, block_freq_verdict = freq.block_frequency(d)
        _, runs_verdict = runs.run_test(d)
        _, longest_run_verdict = runs.longest_one_block_test(d)
        _, fft_verdict = fft.spectral_test(d)
        _, nonoverlap_verdict = matcher.non_overlapping_test(d)
        _, overlap_verdict = matcher.overlapping_patterns(d)
        _, maurer_verdict = maurer.statistical_test(d)
        _, linear_verdict = linear_c.linear_complexity_test(d)
        _, serial_verdict = serial.serial_test(d)[1]
        _, entropy_verdict = entropy.approximate_entropy_test(d)
        _, cusum_forward_verdict = cusum.cumulative_sums_test(d, 0)
        _, cusum_backward_verdict = cusum.cumulative_sums_test(d, 1)
        excursions_data = exc.random_excursions_test(d)
        excursions_var_data = exc.variant_test(d)
    except:
        return False

    excursions_verdict = False
    for excursion in excursions_data:
        excursions_verdict = excursions_verdict and excursion[4]

    excursions_var_verdict = False
    for excursion in excursions_var_data:
        excursions_var_verdict = excursions_var_verdict and excursion[4]

    verdcits = [monobit_verdict, block_freq_verdict, runs_verdict, longest_run_verdict, fft_verdict, nonoverlap_verdict, overlap_verdict, maurer_verdict, linear_verdict, serial_verdict, entropy_verdict, cusum_forward_verdict, cusum_backward_verdict, excursions_verdict, excursions_var_verdict]

    verdicts_counter = Counter(verdcits)

    print(verdicts_counter)

    if verdicts_counter[True] > verdicts_counter[False]:
        return True
    elif verdicts_counter[True] <= verdicts_counter[False]:
        return False