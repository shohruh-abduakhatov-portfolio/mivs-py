import unittest
from src import mc_mivs


class MC_MIVSTest(unittest.TestCase):
    def test_mumtoz_case(self):
        expected = {0: {'prices': {'pred_100': {0: 10, 1: 15}, 'pred_50': {}, 'pred_25': {}, 'cash_cost': {}}, 'total_price': 0,
                        'prepayment_price': 493590}}
        product = ['10716', '10729']
        drug_qnty_req = [10, 15]
        input_capital = 1000000
        cash = 0
        perech = 1000000
        supplier = ['10']
        cash_cost = [[-1], [-1]]
        pred_100 = [[19980], [19586]]
        pred_50 = [[-1], [-1]]
        pred_25 = [[-1], [-1]]
        prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]

        result = mc_mivs.main(product,
                              drug_qnty_req,
                              input_capital,
                              cash,
                              perech,
                              supplier,
                              cash_cost,
                              pred_100,
                              pred_50,
                              pred_25,
                              prices_title)
        self.assertEqual(expected, result)


    def test_num_prod_2(self):
        product = ["drug_A", "drug_B"]
        drug_qnty_req = [10, 10]
        input_capital = 1_000_000_000
        cash = int(input_capital * 0.15)
        perech = input_capital - cash
        supplier = [
            "S1 ",
            "S2 ",
            "S3 ",
            "S4 ",
            "S5 ",
            "S6 ",
            "S7 ",
            "S8 ",
            "S9 ",
            "S10",
            "S11",
            "S12",
            "S13",
            "S14",
            "S15",
            "S16",
            "S17"
        ]
        cash_cost = [
            [661096, 702645, 334348, 549022, 98971, 701367, 516241, 108871, 355646, 278511, 255499, 53295, 193850,
             524844,
             242727, 327308, 237079],  # prod_A
            [197917, 673743, 167629, 146267, 188182, 120858, 448679, 260536, 514830, 410261, 477479, 11253, 489010,
             161398,
             237995, 487019, 178642]]  # prod_B
        pred_100 = [
            [694150, 737777, 351065, 576473, 103919, 736435, 542053, 114314, 373428, 292436, 268273, 55959, 203542,
             551086,
             254863, 343673, 248932],  # prod_A
            [207812, 707430, 176010, 153580, 197591, 126900, 471112, 273562, 540571, 430774, 501352, 11815, 513460,
             169467,
             249894, 511369, 187574]]  # prod_B
        pred_50 = [
            [338811, 360105, 171353, 281373, 50722, 359450, 264573, 55796, 182268, 142736, 130943, 27313, 99348, 268982,
             124397, 167745, 121502],  # prod_A
            [101432, 345293, 85909, 74961, 96443, 61939, 229947, 133524, 263850, 210258, 244707, 5767, 250617, 82716,
             121972, 249597, 91554]]
        pred_25 = [
            [166926, 177417, 84422, 138628, 24990, 177095, 130350, 27489, 89800, 70324, 64513, 13456, 48947, 132523,
             61288,
             82645, 59862],  # prod_A
            [49974, 170120, 42326, 36932, 47515, 30516, 113291, 65785, 129994, 103590, 120563, 2841, 123475, 40752,
             60093,
             122972, 45107]]
        prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
        expected = {
            11: {'prices': {'pred_100': {}, 'pred_50': {}, 'pred_25': {}, 'cash_cost': {0: 10, 1: 10}}, 'total_price': 645480,
                 'prepayment_price': 0}}
        result = mc_mivs.main(product,
                              drug_qnty_req,
                              input_capital,
                              cash,
                              perech,
                              supplier,
                              cash_cost,
                              pred_100,
                              pred_50,
                              pred_25,
                              prices_title)
        self.assertEqual(expected, result)


    def test_num_prod_1(self):
        expected = {11: {'prices': {'pred_100': {}, 'pred_50': {}, 'pred_25': {}, 'cash_cost': {0: 10}}, 'total_price': 532950,
                         'prepayment_price': 0}}
        product = ["drug_A"]
        drug_qnty_req = [10]
        input_capital = 1_000_000_000_000_000
        cash = int(input_capital * 0.15)
        perech = input_capital - cash
        supplier = [
            "Биотехнос, Румыния",
            "ЭВАЛАР",
            "Данафа",
            "НЕОМЕД",
            "Кусум, Индия",
            "Юнифарм, США",
            "Биокад, Россия",
            "Материа Медика, Россия",
            "Феррейн – Россия",
            "Ganga Healthcare, Индия",
            "W – 2",
            "Юник",
            "Новофарм",
            "ГлаксоСмитКлайн, Великобритания",
            "Россия Озон ООО",
            "Лекинтеркапс МЧЖ",
            "Фарм Абиди, Иран"
        ]
        cash_cost = [
            [661096, 702645, 334348, 549022, 98971, 701367, 516241, 108871, 355646, 278511, 255499, 53295, 193850,
             524844,
             242727, 327308, 237079]]
        pred_100 = [
            [694150, 737777, 351065, 576473, 103919, 736435, 542053, 114314, 373428, 292436, 268273, 55959, 203542,
             551086,
             254863, 343673, 248932]]  # prod_B
        pred_50 = [
            [338811, 360105, 171353, 281373, 50722, 359450, 264573, 55796, 182268, 142736, 130943, 27313, 99348, 268982,
             124397, 167745, 121502]]
        pred_25 = [
            [166926, 177417, 84422, 138628, 24990, 177095, 130350, 27489, 89800, 70324, 64513, 13456, 48947, 132523,
             61288,
             82645, 59862]]
        prices_title = ["cash_cost", ["pred_100", "pred_50", "pred_25"]]
        result = mc_mivs.main(product,
                              drug_qnty_req,
                              input_capital,
                              cash,
                              perech,
                              supplier,
                              cash_cost,
                              pred_100,
                              pred_50,
                              pred_25,
                              prices_title)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
