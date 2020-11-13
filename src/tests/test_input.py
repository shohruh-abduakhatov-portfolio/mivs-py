import unittest
from src.tests.data_generator import generate_data_num_2


class MyTestCase(unittest.TestCase):
    def test_something(self):
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
        print()
        product_actual, drug_qnty_req_actual, input_capital_actual, cash_actual, perech_actual, supplier_actual, cash_cost_actual, \
        pred_100_actual, pred_50_actual, pred_25_actual = generate_data_num_2()

        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        self.assertEqual(product, product_actual)
        self.assertEqual(drug_qnty_req, drug_qnty_req_actual)
        self.assertEqual(input_capital, input_capital_actual)
        self.assertEqual(cash, cash_actual)
        self.assertEqual(perech, perech_actual)
        self.assertEqual(supplier, supplier_actual)
        self.assertEqual(cash_cost, cash_cost_actual)
        self.assertEqual(pred_100, pred_100_actual)
        self.assertEqual(pred_50, pred_50_actual)
        self.assertEqual(pred_25, pred_25_actual)



if __name__ == '__main__':
    unittest.main()
