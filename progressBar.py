import time
import os

class ProgressBar(object):
    """
    进度条控件
    """
    def __init__(self, iter_object, description_str=None, width=None, step_str='', tot=None):
        self.iter_object = iter_object
        self.description_str = description_str or 'progress'
        self.tot = tot or len(iter_object)
        self.width = width
        self.step_str = step_str
        self.columns = os.get_terminal_size().columns
        if self.width is None:
            # rows, columns = os.popen('stty size', 'r').read().split()
            self.width = self.columns - 100
    
    def __call__(self):
        return self.step_forward()
    
    def set_step_str(self, step_str):
        self.step_str = step_str

    def step_forward(self):
        print()
        # 先输出一个回到行首
        out_str = '\r'
        # 输出默认的修饰字符串
        out_str += self.description_str
        # 记录进度条开始时间和上次的开始时间
        start_time = time.time()
        last_step_time = start_time
        
        def convert_seconds_to_hms(seconds):
            h, m = 0, 0
            m = seconds // 60
            seconds = int(round(seconds)) % 60
            cost_time = '%ds' % seconds
            if m > 0:
                h = m // 60
                m = int(m) % 60
                cost_time = ('%dm' % m) + cost_time
                h = int(h)
                if h:
                    cost_time = ('%dh' % h) + cost_time
            return cost_time

        for step_idx, element in enumerate(self.iter_object):
            cur_time = time.time()
            # 速度
            speed = max(0, cur_time - last_step_time)
            last_step_time = cur_time
            # 剩余时间
            left_time = (self.tot - step_idx) * speed
            time_cost = cur_time - start_time
            cur_percent = step_idx / self.tot
            step_str = out_str + (' %d/%d (%.2f%%) ' % (step_idx, self.tot, cur_percent * 100))
            bar_width = max(self.width - len(step_str), 10)
            step_str = step_str + '[' + '=' * int(bar_width * cur_percent) + '>' + '.' * (bar_width - int(bar_width * cur_percent)) + ']'
            # 加入时间估计
            step_str += (' - ETA: %s / %s' % (convert_seconds_to_hms(time_cost), convert_seconds_to_hms(left_time)))
            step_str += ' ' + self.step_str
            step_str += ' ' * (self.columns - len(step_str))
            print(step_str, end='')
            yield element
        # 最后来个总结的
        cur_time = time.time()
        time_cost = cur_time - start_time
        step_str = out_str + (' %d / %d (100%%) ' % (self.tot, self.tot))
        bar_width = max(self.width - len(step_str), 10)
        step_str = step_str + '[' + '=' * bar_width + ']'
        step_str += ' - Time: %s' % convert_seconds_to_hms(time_cost)
        step_str += ' ' + self.step_str
        step_str += ' ' * (self.columns - len(step_str))
        print(step_str)
