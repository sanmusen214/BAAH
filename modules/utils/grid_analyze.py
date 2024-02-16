import numpy as np
import cv2
import os
import json
from modules.utils import config

# 走格子：https://bluearchive.wikiru.jp/?10%E7%AB%A0

# move: "left", "right", "left-up", "left-down", "right-up", "right-down", "center"
# exhange： 同上，必定交换。不交换的话用move
# portal: 同上，必定传送。不传送的话用move

class GridAnalyzer:
    """
    走格子类型的战斗的分析器
    
    sol_type是关卡的大类，"quest" 或者 "event", 读取某关的json文件，提供分析方法
    
    此类返回的坐标都是以数组为基底的，即左上角为原点，向下为第一轴正方向，向右为第二轴正方向。如果用于opencv的坐标，需要转换先后。
    """
    
    PIXEL_START_YELLOW = ((125, 250, 250), (132, 255, 255))
    """
    开始时的格子黄色
    """
    PIXEL_MAIN_YELLOW = ((163, 248, 250), (177, 255, 255))
    """
    过程中的聚焦队伍的格子黄色
    """
    # 国服的走格子头顶黄色箭头颜色暗一点,有些关卡敌人会有黄色感叹号(16, 219, 255)
    PIXEL_HEAD_YELLOW_CN_DARKER = ((2, 222, 249), (33, 233, 255))
    # 有些关卡敌人会有黄色感叹号，那个的第一位在40左右，hard关头顶有灯照着时，第一个数字会变暗。
    PIXEL_HEAD_YELLOW = ((4, 223, 254), (33, 235, 255))
    """
    过程中的聚焦队伍的头顶黄色箭头
    """
    # 标准起始方位的角度规定，有个center特殊判断
    START_MAP = {
        '180':"left",
        '0':"right",
        '360':"right",
        '120':"left-up",
        '240':"left-down",
        '60':"right-up",
        '300':"right-down",
        '90':"up",
        '270':"down"
    }
    # 队伍行走方向的距离方位偏，轴与数组轴保持一致
    WALK_MAP = {
        "left":(0, -115),
        "right":(0, 115),
        "left-up":(-80, -60),
        "left-down":(80, -60),
        "right-up":(-80, 60),
        "right-down":(80, 60),
        "center":(0, 0)
    }
    
    def __init__(self, sol_type, jsonfilename) -> None:
        self.jsonfilename = jsonfilename
        # 通过level_data是否为None判断是否读取成功
        self.level_data = None
        self.sol_type = sol_type
        # 尝试读取json文件
        try:
            with open(os.path.join(config.userconfigdict["GRID_SOL_PATH"], self.sol_type, self.jsonfilename), "r", encoding="utf8") as f:
                self.level_data = json.load(f)
        except Exception as e:
            print(e)
            raise Exception("读取关卡json文件失败")

    

    def get_mask(self, img, pixel_range, shrink_kernels=[(3, 3)]):
        """
        提取图片中特定颜色范围的元素，置为白。其他地方置为黑。
        """
        lower = np.array(pixel_range[0])
        upper = np.array(pixel_range[1])
        mask = cv2.inRange(img, lower, upper)
        # 转成灰度图
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        for shrink_kernel in shrink_kernels:
            # 对masker进行腐蚀操作，使用nxn的结构元素
            kernel = np.ones(shrink_kernel, np.uint8)
            mask = cv2.erode(mask, kernel)
        return mask

    def get_kmeans(self, img, n, max_iter=5):
        """
        对白色像素点套用kmeans算法
        
        当输入的图片白色有效像素点不足n个时，会返回loss为-1
        """
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 将img看成二维数组
        # 非0的像素点就是数据点
        # 为0的像素点就是背景
        # 随机n类，每类的中心点（x,y坐标）是随机的
        initial_centers = []
        for i in range(n):
            x = np.random.randint(0, img.shape[0])
            y = np.random.randint(0, img.shape[1])
            initial_centers.append([x, y])
        # print("initial_centers", initial_centers)
        
        centers = initial_centers
        # 每次迭代，每个类的中心点都会更新
        
        # 将图像数组展平
        all_points = img.reshape((-1, 1))
        # 在axis=1的方向上，添加两列，range
        all_points = np.hstack((all_points, np.arange(all_points.shape[0]).reshape((-1, 1))))
        all_points = np.hstack((all_points, np.arange(all_points.shape[0]).reshape((-1, 1))))
        
        # 处理第2列数据除以图像宽度得到整数，处理第3列数据除以图像宽度得到余数
        all_points[:, 1] = all_points[:, 1] // img.shape[1]
        all_points[:, 2] = all_points[:, 2] % img.shape[1]
        # 在axis=1的方向上，添加一列，初始值为0，为每个像素点的类别
        all_points = np.hstack((all_points, np.zeros((all_points.shape[0], 1))))
        # 后续只考虑非0的像素点 np.any(img[i] != 0)
        # 去除第一列为0的像素点
        all_points = all_points[all_points[:, 0] != 0]
        # print("all_points.shape", all_points.shape) # (n, 4)
        
        if all_points.shape[0] == 0:
            print("输入的图片全黑，没有有效像素点")
            return [(-1, -1)], -1
        
        for i in range(max_iter):
            # 每次迭代，计算每个像素点到每个类的距离，取最小的那个类下标赋值给第4列
            for j in range(all_points.shape[0]):
                distances = []
                for k in range(len(centers)):
                    distances.append(np.linalg.norm(all_points[j, 1:3] - centers[k]))
                all_points[j, 3] = np.argmin(distances)
            # 每次迭代，计算每个类的中心点
            for j in range(len(centers)):
                # 取出第4列等于j的所有像素点
                points = all_points[all_points[:, 3] == j]
                # 计算平均值，如果没有像素点（空簇问题），就在其他簇内的点随机挑一个设为这个的中心点
                if points.shape[0] != 0:
                    centers[j] = np.mean(points[:, 1:3], axis=0)
                else:
                    centers[j] = all_points[np.random.randint(0, all_points.shape[0]), 1:3]
            # print("iter centers", centers)
        # 计算最终的centers的失真函数
        loss = 0
        for j in range(len(centers)):
            points = all_points[all_points[:, 3] == j]
            loss += np.sum(np.linalg.norm(points[:, 1:3] - centers[j], axis=1))
        return centers, loss

    def multikmeans(self, img, n, each_max_iter=3, num_of_kmeans=5):
        """
        运行多次kmeans，取loss最小的centers返回，解决零簇问题
        
        没有中心的话会返回loss为-1
        """
        for i in range(num_of_kmeans):
            centers, loss = self.get_kmeans(img, n, each_max_iter)
            if i == 0:
                best_centers = centers
                best_loss = loss
            else:
                if loss < best_loss:
                    best_centers = centers
                    best_loss = loss
        # 计算全局中心点
        # 得到所有centers的中心点
        global_center = np.mean(centers, axis=0)
        return best_centers, best_loss, global_center

    def get_angle(self, start_centers, start_total_center):
        """
        求start_centers里每个点到start_total_center的角度和距离，角度计算以图像右侧，逆时针0-360度为标准
        """
        angles = []
        for center in start_centers:
            angle = np.arctan2(start_total_center[0] - center[0], center[1] - start_total_center[1]) * 180 / np.pi
            if angle < 0:
                angle += 360
            angles.append(angle)
        distances = []
        for center in start_centers:
            distance = np.sqrt((center[0] - start_total_center[0]) ** 2 + (center[1] - start_total_center[1]) ** 2)
            distances.append(distance)
        return angles, distances

    def get_direction(self, angles, distances, direction_list):
        """
        计算angles每个角度，与哪一个direction_list里标准方位的角度最接近，注意靠近360度的角度，要特殊处理
        
        angles: 屏幕上已知的聚类中心点相对角
        direction_list: 攻略说明的队伍初始位置
        """
        # print(direction_list)
        start_map_cv = {}
        
        # 只保留direction_list里有的方位
        for k in self.START_MAP:
            if self.START_MAP[k] in direction_list:
                start_map_cv[k] = self.START_MAP[k]
        # 开始处理，不过先筛选出center
        has_center_ind = -1
        if "center" in direction_list:
            # 找到distances里最小的那个下标作为center_ind
            has_center_ind = distances.index(min(distances))
        # print("start_map_cv", start_map_cv)
        directions = []
        for angle_ind in range(len(angles)):
            angle = angles[angle_ind]
            # 判断是否是center
            if angle_ind == has_center_ind:
                directions.append("center")
                continue
            min_diff = 360
            min_direction = ""
            for key in start_map_cv:
                diff = abs(int(key) - angle)
                if diff < min_diff:
                    min_diff = diff
                    min_direction = start_map_cv[key]
            # 匹配到之后，将键值对从start_map中删除，避免重复匹配
            need_delete = set()
            for key in start_map_cv:
                if start_map_cv[key] == min_direction:
                    need_delete.add(key)
            for key in need_delete:
                start_map_cv.pop(key)
            directions.append(min_direction)
        return directions
    
    def get_requires_list(self):
        """
        获取该关卡可以执行的策略方式名列表
        """
        return self.level_data["requires"]
    
    def get_initialteams(self, require_type):
        """
        获取require_type方案初始的初始队伍配置
        """
        return self.level_data[require_type]["initial_teams"]
    
    def get_num_of_steps(self, require_type):
        """
        获取require_type方案的回合总数
        """
        return len(self.level_data[require_type]["fight_plan"])
    
    def get_action_of_step(self, require_type, step_ind):
        """
        获取require_type方案第step_ind回合的行动，step_ind从0开始
        """
        return self.level_data[require_type]["fight_plan"][step_ind]