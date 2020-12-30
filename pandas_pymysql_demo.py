import pandas as pd
import pymysql as pym


def read_excel():
    excel = pd.read_excel('xxxxx.xlsx')
    excel_contexts = excel.values
    return excel_contexts


def parse_excle(material_id, technology_id, work_procedure_id):
    parse_excel_data = []
    db = pym.connect("xxxxx")
    cursor = db.cursor()

    # 查询物料编码
    sql = "select material_code, item_type from material where id = " + material_id
    cursor.execute(sql)
    results = cursor.fetchall()
    item_type = None
    if len(results) == 0:
        return None
    for row in results:
        parse_excel_data.append(row[0][0])
        item_type = row[0][1]
    # 查询工艺编码
    sql = "select technology_code from technology where id = " + technology_id
    cursor.execute(sql)
    results = cursor.fetchall()
    if len(results) == 0:
        return None
    for row in results:
        parse_excel_data.append(row[0])
    # 查询工序名称
    if item_type is not None:
        if item_type == 1:
            sql = 'select procedure_name from work_procedure where id = ' + work_procedure_id
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                return None
            for row in results:
                parse_excel_data.append(row[0])
        elif item_type == 0:
            sql = 'select procedure_name from work_procedure_product where id = ' + work_procedure_id
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                return None
            for row in results:
                parse_excel_data.append(row[0])
        else:
            return None
    # 拼接其他字段
    parse_excel_data.append("尺寸")
    parse_excel_data.append("")
    parse_excel_data.append("")
    parse_excel_data.append("")
    parse_excel_data.append("")
    parse_excel_data.append("")
    parse_excel_data.append("")
    parse_excel_data.append("1")
    parse_excel_data.append("")
    parse_excel_data.append("")

    # 查询工艺编码
    # 查询工序名称
    db.close()
    return parse_excel_data


def print_excel(parse_data):
    if parse_data is not None and len(parse_data) != 0:
        writer = pd.ExcelWriter('output.xlsx')
        df = pd.DataFrame(
            parse_data, columns=[
                '物料编码', '工艺编码', '工序名称', '质检项目', '上限', '下限', '单位', '首检', '巡检', '自检', '终检', '巡检频率', '自检频率'
            ])
        df.to_excel(writer, index=False)
        writer.save()
        print("输出成功!")
    else:
        print("无数据需要转换!")


if __name__ == '__main__':
    parse_data = []
    temp1 = ["", "", "", "外观", "", "", "", "", "", "", "1", "", ""]
    temp2 = ["", "", "", "螺纹", "", "", "", "", "", "", "1", "", ""]
    count = 0
    for row_data in read_excel():
        print("正在处理第" + str(count) + "个数据")
        count = count + 1
        if count > 100:
            break
        # index: 0 - 物料id
        material_id = row_data[0]
        # index: 1 - 工艺id
        technology_id = row_data[1]
        # index: 2 - 工序id
        work_procedure_id = row_data[2]
        # 添加转换数据
        parse_data_temp = parse_excle(str(material_id), str(technology_id), str(work_procedure_id))
        if parse_data_temp is not None and len(parse_data_temp) != 0:
            parse_data.append(parse_data_temp)
            parse_data.append(temp1)
            parse_data.append(temp2)
        # 将转换后的数据输出为Excel
    print_excel(parse_data)
