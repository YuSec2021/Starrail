import requests
import time
from constant.constant import GACHA_API, JSON_HEADERS, COMMON_ARGUMENT, AUTHKEY
from tools.export_record import ExportGachaRecord


class Gacha(object):
    def __init__(self):
        self.default_res = []
        self.up_role_res = []
        self.up_gz_res = []

        self.proxies = {
            'https': 'http://127.0.0.1:8080',
            'http': 'http://127.0.0.1:8080'
        }

    def get_record_common_func(self, gacha_res, gacha_type=1, end_id=0):
        request_url = '%s?%s&authkey=%s&size=20&gacha_type=%s&end_id=%s' \
                      % (GACHA_API, COMMON_ARGUMENT, AUTHKEY, gacha_type, end_id)
        try:
            res = requests.get(url=request_url, headers=JSON_HEADERS, proxies=self.proxies)
            if res.json():
                end_id = self.get_json(gacha_res, res.json())
                if end_id:
                    time.sleep(1)
                    self.get_record_common_func(gacha_res=gacha_res, gacha_type=gacha_type, end_id=end_id)
        except:
            return {}

    def get_gacha(self):
        # 获取常驻池抽卡数据
        self.get_record_common_func(gacha_res=self.default_res)
        time.sleep(2)

        # # 获取角色池抽卡数据
        gacha_type = 11
        self.get_record_common_func(gacha_res=self.up_role_res, gacha_type=gacha_type)
        time.sleep(2)

        # 获取光锥池抽卡数据
        gacha_type = 12
        self.get_record_common_func(gacha_res=self.up_gz_res, gacha_type=gacha_type)

    def get_json(self, res, gacha_json):
        if len(gacha_json['data']['list']) == 0:
            return 0

        for i in gacha_json['data']['list']:
            res.append(i)
        return res[-1]['id']

    def record_data_analysis(self, res):
        rank_type = {'3': 0, '4': 0, '5': 0}
        for i in res:
            if i['rank_type'] == '5':
                print("%s: %s" % (i['item_type'], i['name']))
                rank_type['5'] += 1
            elif i['rank_type'] == '4':
                rank_type['4'] += 1
            elif i['rank_type'] == '3':
                rank_type['3'] += 1

        print("5星占比为：%.2f，个数为：%d" % (rank_type['5']/len(res), rank_type['5']))
        print("4星占比为：%.2f，个数为：%d" % (rank_type['4']/len(res), rank_type['4']))
        print("3星占比为：%.2f，个数为：%d" % (rank_type['3']/len(res), rank_type['3']))
        print("5星出货率：%.2f" % (len(res)/rank_type['5']))

    def print_data(self):
        print("光锥池数据：")
        print("光锥抽卡池次数：", len(self.up_gz_res))
        print("光锥池五星：")
        self.record_data_analysis(self.up_gz_res)

        print('----------------------------------------------------------')

        print("角色池数据：")
        print("角色池抽卡次数：", len(self.up_role_res))
        print("角色池5星：")
        self.record_data_analysis(self.up_role_res)

        print('----------------------------------------------------------')

        print("常驻池数据：")
        print("常驻池抽卡次数：", len(self.default_res))
        print("常驻池五星：")
        self.record_data_analysis(self.default_res)

    def export_data(self, workdir):
        e = ExportGachaRecord(workdir)
        e.export_gacha_record(gacha_type=11, gacha_res=self.up_gz_res)
        e.export_gacha_record(gacha_type=12, gacha_res=self.up_role_res)
        e.export_gacha_record(gacha_type=1, gacha_res=self.default_res)

    def run(self):
        print("获取数据")
        self.get_gacha()

        print("导出数据")
        self.export_data('')

        print("打印抽卡详情")
        self.print_data()





