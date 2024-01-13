import matplotlib
matplotlib.use('Agg')  # 设置为非交互式后端
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.font_manager import FontProperties

# 找到当前目录
current_dir = os.path.dirname(os.path.abspath(__file__))
font_file_path = os.path.join(current_dir, 'AlibabaPuHuiTi-3-45-Light.ttf')
chart_font = FontProperties(fname=font_file_path)

# 设置 matplotlib 字体支持中文
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


class ChartLine:
    data_sample = """
        {
          "title": "各商品的销售额",
          "x_label": "时间（月份）",
          "y_label": "销售额（元）",
          "x_data": [1, 2, 3, 4, 5],
          "lines": [
            {
              "y_data": [2, 3, 5, 7, 11],
              "legend": "电脑"
            },
            {
              "y_data": [1, 4, 9, 16, 25],
              "legend": "手机"
            }
          ]
        }
        """

    data_requires = """
        1. x_data 和 y_data 的长度必须一致。
        2. lines 需要根据实际情况来生成，可以有1条或多条
        3. x_label 和 y_label 若有单位，需要包含单位，若不清楚可以不带；
        """

    @classmethod
    def gen_image(cls, data, image_file_path):
        # 生成折线图
        # 创建一个新的图形和轴实例
        fig, ax = plt.subplots()

        ax.set_title(
            data["title"],
            fontproperties=chart_font
        )
        ax.set_xlabel(data["x_label"],
                      fontproperties=chart_font
                      )
        ax.set_ylabel(data["y_label"],
                      fontproperties=chart_font
                      )

        for line in data["lines"]:
            ax.plot(data["x_data"], line["y_data"], label=line["legend"])

        ax.legend(
            prop=chart_font
        )
        fig.savefig(image_file_path)
        plt.close(fig)  # 关闭图形以释放资源


class ChartPie:
    data_sample = """
        {
          "title": "各商品的销量",
          "labels": ["手机", "电脑", "显示器", "键盘"],
          "sizes": [15, 30, 20, 10]
        }
        """
    data_requires = """
        1. labels 和 sizes 的长度必须一致。
        """



    @classmethod
    def gen_image(cls, data, image_file_path):
        # 生成饼图

        def make_autopct(sizes):
            def my_autopct(pct):
                total = sum(sizes)
                val = int(round(pct * total / 100.0))
                return '{p:.1f}%\n({v:d})'.format(p=pct, v=val)

            return my_autopct

        # 创建一个新的图形和轴实例
        fig, ax = plt.subplots()

        # 设置标题并生成饼图
        ax.set_title(data["title"],
                     fontproperties=chart_font
                     )
        ax.pie(data["sizes"], labels=data["labels"],
               autopct=make_autopct(data["sizes"]),
               textprops={'fontproperties': chart_font}
               )

        # 设置轴，保证饼图是圆的
        ax.axis('equal')

        # 保存图像到文件
        fig.savefig(image_file_path)

        # 关闭图形以释放资源
        plt.close(fig)


class ChartBar:

    data_sample = """
        {
          "title": "各商品销量",
          "x_label": "类别",
          "y_label": "销售额（万元）",
          "categories": ["手机", "电脑", "显示器", "键盘"],
          "datasets": [
            {
              "label": "1月份",
              "values": [10, 20, 30, 40]
            },
            {
              "label": "2月份",
              "values": [15, 25, 35, 45]
            }
          ]
        }
        """

    data_requires = """
        1. categories 和 values 的长度必须一致。
        2. datasets 需要根据实际情况来生成，可以有1个或多个
        3. 
    """

    @classmethod
    def gen_image(cls, data, image_file_path):
        # 绘制柱状图
        fig, ax = plt.subplots()
        num_categories = len(data["categories"])
        bar_width = 0.35  # 柱子的宽度
        index = np.arange(num_categories)

        for i, dataset in enumerate(data["datasets"]):
            ax.bar(index + i * bar_width, dataset["values"], bar_width, label=dataset["label"])

        ax.set_xlabel(data["x_label"],
                      fontproperties=chart_font
                      )
        ax.set_ylabel(data["y_label"],
                      fontproperties=chart_font
                      )
        ax.set_title(data["title"],
                     fontproperties=chart_font
                     )
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(data["categories"],
                           fontproperties=chart_font
                           )
        ax.legend(
            prop=chart_font
        )
        fig.savefig(image_file_path)
        plt.close(fig)  # 关闭图形以释放资源


def gen_image(chart_type, chart_data, image_file_path):
    if chart_type == 'line':
        ChartLine.gen_image(chart_data, image_file_path)
    elif chart_type == 'bar':
        ChartBar.gen_image(chart_data, image_file_path)
    elif chart_type == 'pie':
        ChartPie.gen_image(chart_data, image_file_path)
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")


if __name__ == '__main__':
    # 生成折线图
    import json
    ChartLine.gen_image(json.loads(ChartLine.data_sample), "line.png")
    ChartBar.gen_image(json.loads(ChartBar.data_sample), "bar.png")
    ChartPie.gen_image(json.loads(ChartPie.data_sample), "pie.png")
