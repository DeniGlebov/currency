import os

from django.conf import settings

from rate.models import Rate
from rate.tasks import parse_aval, parse_monobank, parse_nbu, parse_oschadbank, parse_privatbank, parse_vkurse


class Response:
    pass


def test_privat(mocker):
    def mock():
        res = [
            {"ccy": "USD", "base_ccy": "UAH", "buy": "27.45000", "sale": "27.86000"},
            {"ccy": "EUR", "base_ccy": "UAH", "buy": "32.30000", "sale": "33.01000"},
            {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.36000", "sale": "0.38800"},
            {"ccy": "BTC", "base_ccy": "USD", "buy": "11017.6036", "sale": "12177.3514"},
        ]
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_privatbank()
    assert Rate.objects.count() == rate_initial_count + 6
    parse_privatbank()


def test_parse_monobank(mocker):
    def mock():
        res = [
            {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1596229809, "rateBuy": 27.6, "rateSell": 27.8552},
            {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1596263409, "rateBuy": 32.35, "rateSell": 32.95},
            {"currencyCodeA": 643, "currencyCodeB": 980, "date": 1596262809, "rateBuy": 0.363, "rateSell": 0.388},
            {"currencyCodeA": 978, "currencyCodeB": 840, "date": 1596262809, "rateBuy": 1.17, "rateSell": 1.187},
            {"currencyCodeA": 985, "currencyCodeB": 980, "date": 1596290294, "rateBuy": 7.27, "rateSell": 7.47,
             "rateCross": 7.4697},
            {"currencyCodeA": 826, "currencyCodeB": 980, "date": 1596290244, "rateCross": 36.2395},
            {"currencyCodeA": 392, "currencyCodeB": 980, "date": 1596288070, "rateCross": 0.2651},
            {"currencyCodeA": 756, "currencyCodeB": 980, "date": 1596289884, "rateCross": 30.5029},
            {"currencyCodeA": 156, "currencyCodeB": 980, "date": 1596289589, "rateCross": 3.9747},
            {"currencyCodeA": 784, "currencyCodeB": 980, "date": 1596288629, "rateCross": 7.5832},
            {"currencyCodeA": 971, "currencyCodeB": 980, "date": 1594192561, "rateCross": 0.3528},
            {"currencyCodeA": 8, "currencyCodeB": 980, "date": 1596289745, "rateCross": 0.2669},
            {"currencyCodeA": 51, "currencyCodeB": 980, "date": 1596287319, "rateCross": 0.0575},
            {"currencyCodeA": 973, "currencyCodeB": 980, "date": 1583268835, "rateCross": 0.0509},
            {"currencyCodeA": 32, "currencyCodeB": 980, "date": 1596290107, "rateCross": 0.3853},
            {"currencyCodeA": 36, "currencyCodeB": 980, "date": 1596287994, "rateCross": 19.9392},
            {"currencyCodeA": 944, "currencyCodeB": 980, "date": 1596273470, "rateCross": 16.3913},
            {"currencyCodeA": 50, "currencyCodeB": 980, "date": 1596033036, "rateCross": 0.3276},
            {"currencyCodeA": 975, "currencyCodeB": 980, "date": 1596290137, "rateCross": 16.8004},
            {"currencyCodeA": 48, "currencyCodeB": 980, "date": 1595836651, "rateCross": 74.1625},
            {"currencyCodeA": 108, "currencyCodeB": 980, "date": 1538606522, "rateCross": 0.0158},
            {"currencyCodeA": 96, "currencyCodeB": 980, "date": 1593518156, "rateCross": 19.1978},
            {"currencyCodeA": 68, "currencyCodeB": 980, "date": 1591125688, "rateCross": 3.9198},
            {"currencyCodeA": 986, "currencyCodeB": 980, "date": 1596286362, "rateCross": 5.4036},
            {"currencyCodeA": 72, "currencyCodeB": 980, "date": 1596284818, "rateCross": 2.4171},
            {"currencyCodeA": 933, "currencyCodeB": 980, "date": 1596290292, "rateCross": 11.4194},
            {"currencyCodeA": 124, "currencyCodeB": 980, "date": 1596290113, "rateCross": 20.8307},
            {"currencyCodeA": 976, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.0143},
            {"currencyCodeA": 152, "currencyCodeB": 980, "date": 1596287050, "rateCross": 0.037},
            {"currencyCodeA": 170, "currencyCodeB": 980, "date": 1596290191, "rateCross": 0.0074},
            {"currencyCodeA": 188, "currencyCodeB": 980, "date": 1596242536, "rateCross": 0.0477},
            {"currencyCodeA": 192, "currencyCodeB": 980, "date": 1596229809, "rateCross": 27.6},
            {"currencyCodeA": 203, "currencyCodeB": 980, "date": 1596290244, "rateCross": 1.2493},
            {"currencyCodeA": 262, "currencyCodeB": 980, "date": 1583847065, "rateCross": 0.1462},
            {"currencyCodeA": 208, "currencyCodeB": 980, "date": 1596289582, "rateCross": 4.4042},
            {"currencyCodeA": 12, "currencyCodeB": 980, "date": 1591275793, "rateCross": 0.2089},
            {"currencyCodeA": 818, "currencyCodeB": 980, "date": 1596290288, "rateCross": 1.7501},
            {"currencyCodeA": 230, "currencyCodeB": 980, "date": 1581262962, "rateCross": 0.7724},
            {"currencyCodeA": 981, "currencyCodeB": 980, "date": 1596290251, "rateCross": 9.0666},
            {"currencyCodeA": 936, "currencyCodeB": 980, "date": 1592625807, "rateCross": 4.6343},
            {"currencyCodeA": 270, "currencyCodeB": 980, "date": 1576592087, "rateCross": 0.493},
            {"currencyCodeA": 324, "currencyCodeB": 980, "date": 1581349536, "rateCross": 0.0025},
            {"currencyCodeA": 344, "currencyCodeB": 980, "date": 1596232544, "rateCross": 3.5941},
            {"currencyCodeA": 191, "currencyCodeB": 980, "date": 1596290228, "rateCross": 4.4122},
            {"currencyCodeA": 348, "currencyCodeB": 980, "date": 1596290051, "rateCross": 0.0949},
            {"currencyCodeA": 360, "currencyCodeB": 980, "date": 1596288551, "rateCross": 0.0019},
            {"currencyCodeA": 376, "currencyCodeB": 980, "date": 1596289973, "rateCross": 8.195},
            {"currencyCodeA": 356, "currencyCodeB": 980, "date": 1596286302, "rateCross": 0.3729},
            {"currencyCodeA": 368, "currencyCodeB": 980, "date": 1596032437, "rateCross": 0.0233},
            {"currencyCodeA": 364, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.0007},
            {"currencyCodeA": 352, "currencyCodeB": 980, "date": 1596220520, "rateCross": 0.2057},
            {"currencyCodeA": 400, "currencyCodeB": 980, "date": 1596289789, "rateCross": 39.2781},
            {"currencyCodeA": 404, "currencyCodeB": 980, "date": 1596280883, "rateCross": 0.2584},
            {"currencyCodeA": 417, "currencyCodeB": 980, "date": 1596270457, "rateCross": 0.3629},
            {"currencyCodeA": 116, "currencyCodeB": 980, "date": 1589974339, "rateCross": 0.0065},
            {"currencyCodeA": 408, "currencyCodeB": 980, "date": 1596229809, "rateCross": 12.5454},
            {"currencyCodeA": 410, "currencyCodeB": 980, "date": 1596285276, "rateCross": 0.0234},
            {"currencyCodeA": 414, "currencyCodeB": 980, "date": 1596094082, "rateCross": 90.785},
            {"currencyCodeA": 398, "currencyCodeB": 980, "date": 1596289185, "rateCross": 0.066},
            {"currencyCodeA": 418, "currencyCodeB": 980, "date": 1596272261, "rateCross": 0.003},
            {"currencyCodeA": 422, "currencyCodeB": 980, "date": 1596142592, "rateCross": 0.0185},
            {"currencyCodeA": 144, "currencyCodeB": 980, "date": 1596284058, "rateCross": 0.15},
            {"currencyCodeA": 434, "currencyCodeB": 980, "date": 1596229809, "rateCross": 20.1342},
            {"currencyCodeA": 504, "currencyCodeB": 980, "date": 1596254045, "rateCross": 2.9793},
            {"currencyCodeA": 498, "currencyCodeB": 980, "date": 1596287272, "rateCross": 1.673},
            {"currencyCodeA": 969, "currencyCodeB": 980, "date": 1587685421, "rateCross": 0.0071},
            {"currencyCodeA": 807, "currencyCodeB": 980, "date": 1596280987, "rateCross": 0.5348},
            {"currencyCodeA": 496, "currencyCodeB": 980, "date": 1578446963, "rateCross": 0.0089},
            {"currencyCodeA": 478, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.0728},
            {"currencyCodeA": 480, "currencyCodeB": 980, "date": 1596092068, "rateCross": 0.6976},
            {"currencyCodeA": 454, "currencyCodeB": 980, "date": 1581405226, "rateCross": 0.0337},
            {"currencyCodeA": 484, "currencyCodeB": 980, "date": 1596251479, "rateCross": 1.2688},
            {"currencyCodeA": 458, "currencyCodeB": 980, "date": 1596283662, "rateCross": 6.5604},
            {"currencyCodeA": 943, "currencyCodeB": 980, "date": 1595773690, "rateCross": 0.4007},
            {"currencyCodeA": 516, "currencyCodeB": 980, "date": 1586304458, "rateCross": 1.4044},
            {"currencyCodeA": 566, "currencyCodeB": 980, "date": 1596155208, "rateCross": 0.0716},
            {"currencyCodeA": 558, "currencyCodeB": 980, "date": 1584744612, "rateCross": 0.8389},
            {"currencyCodeA": 578, "currencyCodeB": 980, "date": 1596290011, "rateCross": 3.0626},
            {"currencyCodeA": 524, "currencyCodeB": 980, "date": 1596205176, "rateCross": 0.2324},
            {"currencyCodeA": 554, "currencyCodeB": 980, "date": 1596213999, "rateCross": 18.5527},
            {"currencyCodeA": 512, "currencyCodeB": 980, "date": 1596181831, "rateCross": 72.368},
            {"currencyCodeA": 604, "currencyCodeB": 980, "date": 1596238335, "rateCross": 7.8948},
            {"currencyCodeA": 608, "currencyCodeB": 980, "date": 1596253201, "rateCross": 0.5671},
            {"currencyCodeA": 586, "currencyCodeB": 980, "date": 1596289044, "rateCross": 0.1671},
            {"currencyCodeA": 600, "currencyCodeB": 980, "date": 1584323182, "rateCross": 0.0041},
            {"currencyCodeA": 634, "currencyCodeB": 980, "date": 1596259541, "rateCross": 7.6508},
            {"currencyCodeA": 946, "currencyCodeB": 980, "date": 1596288442, "rateCross": 6.8177},
            {"currencyCodeA": 941, "currencyCodeB": 980, "date": 1596290138, "rateCross": 0.2793},
            {"currencyCodeA": 682, "currencyCodeB": 980, "date": 1596280429, "rateCross": 7.428},
            {"currencyCodeA": 690, "currencyCodeB": 980, "date": 1596204542, "rateCross": 1.5676},
            {"currencyCodeA": 938, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.5018},
            {"currencyCodeA": 752, "currencyCodeB": 980, "date": 1596290036, "rateCross": 3.1829},
            {"currencyCodeA": 702, "currencyCodeB": 980, "date": 1596288139, "rateCross": 20.3526},
            {"currencyCodeA": 694, "currencyCodeB": 980, "date": 1595787606, "rateCross": 0.0028},
            {"currencyCodeA": 706, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.048},
            {"currencyCodeA": 968, "currencyCodeB": 980, "date": 1591303043, "rateCross": 3.5865},
            {"currencyCodeA": 760, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.022},
            {"currencyCodeA": 748, "currencyCodeB": 980, "date": 1596229809, "rateCross": 1.6538},
            {"currencyCodeA": 764, "currencyCodeB": 980, "date": 1596288944, "rateCross": 0.8871},
            {"currencyCodeA": 972, "currencyCodeB": 980, "date": 1596177195, "rateCross": 2.7014},
            {"currencyCodeA": 795, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.0016},
            {"currencyCodeA": 788, "currencyCodeB": 980, "date": 1596247075, "rateCross": 10.2367},
            {"currencyCodeA": 949, "currencyCodeB": 980, "date": 1596290299, "rateCross": 3.9925},
            {"currencyCodeA": 901, "currencyCodeB": 980, "date": 1596272172, "rateCross": 0.9484},
            {"currencyCodeA": 834, "currencyCodeB": 980, "date": 1595112020, "rateCross": 0.012},
            {"currencyCodeA": 800, "currencyCodeB": 980, "date": 1595859077, "rateCross": 0.0075},
            {"currencyCodeA": 858, "currencyCodeB": 980, "date": 1596189880, "rateCross": 0.6568},
            {"currencyCodeA": 860, "currencyCodeB": 980, "date": 1596124096, "rateCross": 0.0027},
            {"currencyCodeA": 704, "currencyCodeB": 980, "date": 1596288914, "rateCross": 0.0012},
            {"currencyCodeA": 950, "currencyCodeB": 980, "date": 1595672715, "rateCross": 0.0493},
            {"currencyCodeA": 952, "currencyCodeB": 980, "date": 1596281426, "rateCross": 0.0499},
            {"currencyCodeA": 886, "currencyCodeB": 980, "date": 1543715495, "rateCross": 0.112},
            {"currencyCodeA": 710, "currencyCodeB": 980, "date": 1596284043, "rateCross": 1.6686},
            {"currencyCodeA": 894, "currencyCodeB": 980, "date": 1596229809, "rateCross": 0.0015}
        ]
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_monobank()
    assert Rate.objects.count() == rate_initial_count + 6
    parse_monobank()


def test_parse_nbu(mocker):
    def mock():
        res = [
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "036", "CurrencyCodeL": "AUD",
                "Units": 1, "Amount": 19.881
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "944", "CurrencyCodeL": "AZN",
                "Units": 1, "Amount": 16.2392
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "933", "CurrencyCodeL": "BYN",
                "Units": 1, "Amount": 11.3367
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "975", "CurrencyCodeL": "BGN",
                "Units": 1, "Amount": 16.7634
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "410", "CurrencyCodeL": "KRW",
                "Units": 100, "Amount": 2.324
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "344", "CurrencyCodeL": "HKD",
                "Units": 1, "Amount": 3.5715
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "208", "CurrencyCodeL": "DKK",
                "Units": 1, "Amount": 4.4037
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "840", "CurrencyCodeL": "USD",
                "Units": 1, "Amount": 27.6798
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "978", "CurrencyCodeL": "EUR",
                "Units": 1, "Amount": 32.7812
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "818", "CurrencyCodeL": "EGP",
                "Units": 1, "Amount": 1.7331
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "392", "CurrencyCodeL": "JPY",
                "Units": 10, "Amount": 2.6376
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "985", "CurrencyCodeL": "PLN",
                "Units": 1, "Amount": 7.444
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "356", "CurrencyCodeL": "INR",
                "Units": 10, "Amount": 3.7001
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "124", "CurrencyCodeL": "CAD",
                "Units": 1, "Amount": 20.6166
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "191", "CurrencyCodeL": "HRK",
                "Units": 1, "Amount": 4.3814
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "484", "CurrencyCodeL": "MXN",
                "Units": 1, "Amount": 1.2481
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "498", "CurrencyCodeL": "MDL",
                "Units": 1, "Amount": 1.6513
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "376", "CurrencyCodeL": "ILS",
                "Units": 1, "Amount": 8.1366
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "554", "CurrencyCodeL": "NZD",
                "Units": 1, "Amount": 18.4486
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "578", "CurrencyCodeL": "NOK",
                "Units": 1, "Amount": 3.0535
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "710", "CurrencyCodeL": "ZAR",
                "Units": 1, "Amount": 1.6346
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "643", "CurrencyCodeL": "RUB",
                "Units": 10, "Amount": 3.7387
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "946", "CurrencyCodeL": "RON",
                "Units": 1, "Amount": 6.7846
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "360", "CurrencyCodeL": "IDR",
                "Units": 1000, "Amount": 1.8955
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "682", "CurrencyCodeL": "SAR",
                "Units": 1, "Amount": 7.3797
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "702", "CurrencyCodeL": "SGD",
                "Units": 1, "Amount": 20.1807
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "960", "CurrencyCodeL": "XDR",
                "Units": 1, "Amount": 39.1055
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "398", "CurrencyCodeL": "KZT",
                "Units": 100, "Amount": 6.5657
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "949", "CurrencyCodeL": "TRY",
                "Units": 1, "Amount": 3.9712
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "348", "CurrencyCodeL": "HUF",
                "Units": 100, "Amount": 9.493
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "826", "CurrencyCodeL": "GBP",
                "Units": 1, "Amount": 36.3989
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "203", "CurrencyCodeL": "CZK",
                "Units": 1, "Amount": 1.2525
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "752", "CurrencyCodeL": "SEK",
                "Units": 1, "Amount": 3.1869
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "756", "CurrencyCodeL": "CHF",
                "Units": 1, "Amount": 30.4458
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "156", "CurrencyCodeL": "CNY",
                "Units": 1, "Amount": 3.9686
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "012", "CurrencyCodeL": "DZD",
                "Units": 10, "Amount": 2.1575
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "764", "CurrencyCodeL": "THB",
                "Units": 10, "Amount": 8.8726
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "986", "CurrencyCodeL": "BRL",
                "Units": 1, "Amount": 5.3502
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "051", "CurrencyCodeL": "AMD",
                "Units": 100, "Amount": 5.7033
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "936", "CurrencyCodeL": "GHS",
                "Units": 1, "Amount": 4.804
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "784", "CurrencyCodeL": "AED",
                "Units": 1, "Amount": 7.536
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "704", "CurrencyCodeL": "VND",
                "Units": 1000, "Amount": 1.1948
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "368", "CurrencyCodeL": "IQD",
                "Units": 100, "Amount": 2.326
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "364", "CurrencyCodeL": "IRR",
                "Units": 10000, "Amount": 6.5904
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "981", "CurrencyCodeL": "GEL",
                "Units": 1, "Amount": 8.9986
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "422", "CurrencyCodeL": "LBP",
                "Units": 100, "Amount": 1.8361
            },
            {
                "StartDate": "03.08.2020", "TimeSign": "0000", "CurrencyCode": "434", "CurrencyCodeL": "LYD",
                "Units": 1, "Amount": 20.1425
            },
        ]

        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_nbu()
    assert Rate.objects.count() == rate_initial_count + 6
    parse_nbu()


def test_parse_vkurse(mocker):
    def mock():
        res = {
            "Dollar": {
                "buy": "27.55",
                "sale": "27.80"
            },
            "Euro": {
                "buy": "32.35",
                "sale": "32.65"
            },
            "Rub": {
                "buy": "0.368",
                "sale": "0.377"
            },
            "Rub123": {
                "buy": "0.368",
                "sale": "0.377"
            }
        }
        response = Response()
        response.json = lambda: res
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    rate_initial_count = Rate.objects.count()
    parse_vkurse()
    assert Rate.objects.count() == rate_initial_count + 6
    parse_vkurse()


def test_parse_oschadbank(mocker):
    def mock():
        path = os.path.join(settings.BASE_DIR, 'tests', 'html', 'oschadbank.html')
        with open(path) as file:
            content = file.read()

        response = Response()
        response.status_code = 200
        response.text = content
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    parse_oschadbank()


def test_aval(mocker):
    def mock():
        path = os.path.join(settings.BASE_DIR, 'tests', 'html', 'aval.html')
        with open(path) as file:
            content = file.read()

        response = Response()
        response.status_code = 200
        response.text = content
        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()
    parse_aval()
