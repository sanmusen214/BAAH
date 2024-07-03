from nicegui import ui
from modules.configs.MyConfig import config

def list_edit_area(datadict, linedesc, blockdesc="", has_switch=False):
    """
    datadict: 要修改的二维或三维列表，长度代表列表维度
        [str1, str2] 或 [str1, str2, [str3, str4]] 或 [str1, str2, [str3, str4, str5]]
    linedesc: 二维或三维列表的描述，长度代表列表维度
    blockdesc: 对于这个块的描述
    has_switch: 是否有功能开关
    """
    dim = len(linedesc)
    # 对列表的最后一维的元素的文字描述的数量
    # [关卡，次数] -> subdim = 2 = len(linedesc[2])
    # [地区，关卡，次数] -> subdim = 3 = len(linedesc[2])
    subdim = 0
    if dim >= 3:
        subdim = len(linedesc[2])
    @ui.refreshable
    def item_list():
        for blocklinedesc in blockdesc.split('\n'):
            ui.label(f'{blocklinedesc}')
        for i in range(len(datadict)):
            line_item = datadict[i]
            ui.label(f'{config.get_text("config_nth")} {i+1} {linedesc[0]}: ')
            with ui.row():
                for j in range(len(line_item)):
                    if len(linedesc) == 2:
                        # 第几个教室
                        ui.number(f'{linedesc[1]}',
                                    min=1,
                                    step=1,
                                    precision=0,
                                    format="%.0f",
                                    value=line_item[j],
                                    on_change=lambda v,i=i,j=j: datadict[i].__setitem__(j, int(v.value)),
                                    ).style('width: 60px')
                    elif len(linedesc) == 3:
                        ui.label(f'{linedesc[1]}:')
                        with ui.row():
                            with ui.card():
                                for k in range(len(line_item[j])):
                                    # 如果一个元素的数据量超出了给定的文字描述的数量，而且是有开关的
                                    # 那么最后那个'多出来的'数据就是开关
                                    if k >= subdim: # 多出来的数据下标continue掉，没有对应的渲染文字
                                        if k == subdim and has_switch: # 如果刚好多一个数据而且has_switch就渲染个开关
                                            ui.label(config.get_text("button_enable"))
                                            ui.switch(value=line_item[j][k],on_change=lambda v,i=i,j=j:datadict[i][j].__setitem__(k, bool(v.value)))
                                        continue
                                    #  遍历地区, 关卡和次数
                                    min_value = 1
                                    # 如果数据的位置就是最后一个文字描述的位置，代表的数据是扫荡次数，最小值为-99
                                    if k == subdim-1:
                                        min_value = -99
                                    ui.number(f'{linedesc[2][k]}',
                                                min=min_value,
                                                step=1,
                                                precision=0,
                                                format="%.0f",
                                                value=line_item[j][k],
                                                on_change=lambda v,i=i,j=j,k=k: datadict[i][j].__setitem__(k, int(v.value)),
                                                ).style('width: 60px')
                with ui.column():
                    ui.button(f"{config.get_text('button_add')} {linedesc[1]}", on_click=lambda i=i: add_item_item(i))
                    if len(datadict[i]) > 0:
                        ui.button(f"{config.get_text('button_delete')} {linedesc[1]}", on_click=lambda i=i: del_item_item(i), color="red")
        with ui.row():
            ui.button(f"{config.get_text('button_add')} {linedesc[0]}", on_click=add_item)
            if len(datadict) > 0:
                ui.button(f"{config.get_text('button_delete')} {linedesc[0]}", on_click=del_item, color="red")
 
    def add_item():
        datadict.append([])
        item_list.refresh()
    
    def del_item():
        datadict.pop()
        item_list.refresh()
    
    def add_item_item(item_ind):
        if dim == 2:
            datadict[item_ind].append(1)
        elif dim == 3:
            if subdim == 2:
                if has_switch:
                    datadict[item_ind].append([1, 1, True])
                else:
                    datadict[item_ind].append([1, 1])
            elif subdim == 3:
                if has_switch:
                    datadict[item_ind].append([1, 1, 1, True])
                else:
                    datadict[item_ind].append([1, 1, 1])
        
        item_list.refresh()
    
    def del_item_item(item_ind):
        datadict[item_ind].pop()
        item_list.refresh()

    item_list()