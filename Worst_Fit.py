import random
import time
from Process import Process
from Mem_Seg import Mem_Seg
from Memory import Memory

class Worst_fit:

    def initialize(self, canvas):

        canvas.update()
        canvas.delete('all')

        # instantiate and create grid
        grd = Memory()
        grd.create_grid(canvas)

        proc_list = []
        mem_seg = []
        mem_seg_free = []

        # processes color
        proc_color = 'green'

        for i in range(50):
            # random number for burst time
            rdn_bt = random.randint(3, 7)
            # random number for arrival time
            rdn_at = random.randint(1, 50)
            # random number for size
            rdn_size = random.randint(1, 40)
            # set process name
            p_name = "p" + str(i)
            p = Process(id_p=i, name=p_name, burst_time=rdn_bt, color=proc_color, arrival_time=rdn_at, size=rdn_size)
            proc_list.append(p)

        # prepare memory/create 4 segments already filled
        x = 100
        x_bfr = 50
        for i in range(4):
            rdn_x1 = random.randint(x_bfr, x_bfr + 100)
            rdn_x2 = random.randint(rdn_x1, rdn_x1 + 100)
            seg = canvas.create_rectangle(rdn_x1, 20, rdn_x2, 70, fill='#4785e8')
            print("I: ", str(i))
            print("X1: ", str(rdn_x1))
            print("X2: ", str(rdn_x2))
            dif_size = rdn_x2 - rdn_x1
            mg = Mem_Seg(name_ms="f" + str(i),
                         id_ms=i,
                         space=dif_size,
                         x1=rdn_x1,
                         x2=rdn_x2)
            mem_seg.append(mg)

            x_bfr = rdn_x2
            x = x + 100

        # define memory segmentation with these settings
        for idx in range(len(mem_seg)):
            # verify if it is the first occupied segment/OK
            if idx == 0:
                if mem_seg[idx].x1 > 50:
                    segment = Mem_Seg(name_ms="f" + str(i + 3),
                                      id_ms=i + 3,
                                      space=mem_seg[idx].x1 - 50,
                                      x1=50,
                                      x2=mem_seg[idx].x1)
                    mem_seg_free.append(segment)
            else:
                # if the segment is in the middle/OK
                if mem_seg[idx].x1 > mem_seg[idx - 1].x2:
                    segment = Mem_Seg(name_ms="f" + str(i + 3),
                                      id_ms=i + 3,
                                      space=mem_seg[idx].x1 - mem_seg[idx - 1].x2,
                                      x1=mem_seg[idx - 1].x2,
                                      x2=mem_seg[idx].x1)
                    mem_seg_free.append(segment)
                # if it is the last segment
                if idx == len(mem_seg) - 1:
                    if mem_seg[idx].x2 != 800:
                        segment = Mem_Seg(name_ms="f" + str(i + 3),
                                          id_ms=i + 3,
                                          space=800 - mem_seg[idx].x2,
                                          x1=mem_seg[idx].x2,
                                          x2=800)
                        mem_seg_free.append(segment)

        return mem_seg_free, proc_list, mem_seg

    def Worst_fit_run(self,canvas):

        # initialize method
        response = self.initialize(canvas)
        mem_seg_f = response[0]
        list_p = response[1]
        mem_seg = response[2]

        for proce in list_p:
            print(str(proce.name) + " | " + str(proce.size))

        # set settings for process
        font_settings_proc = ('Courier New', '22')

        proc_text = canvas.create_text(120, 120, text='Processes: ', font=font_settings_proc, tag="proc_text")
        proc_num = canvas.create_text(200, 120, text='0', font=font_settings_proc)

        canvas.create_text(205, 160, text='Process Representation: ', font=font_settings_proc)

        i = 0
        p = 0
        j = 150

        # list for waiting process
        wait_list = []

        while len(list_p) >= 0:

            delete_p = False
            if len(list_p) == 0:
                canvas.itemconfig(proc_num, text=str(len(list_p)))
                break

            # verify wait list and execute process
            if len(wait_list) > 0:
                # fazer loop na lista e diminui o burst time
                for proc_w in wait_list:
                    proc_w.burst_time = proc_w.burst_time - 1
                    if proc_w.burst_time == 0:
                        # remove process
                        wait_list.remove(proc_w)
                        # delete process
                        # retirar a representacao grafica
                        canvas.delete(str(proc_w.name))
                        # removing segment from segment list
                        for segment_s in mem_seg:
                            if segment_s.name_ms == proc_w.name:
                                mem_seg.remove(segment_s)
                        # update canvas
                        canvas.update()
                        # reset free segments
                        mem_seg_f = []
                        # creating new free segments
                        for idx in range(len(mem_seg)):
                            # verify if it is the first occupied segment/OK
                            if idx == 0:
                                if mem_seg[idx].x1 > 50:
                                    segment = Mem_Seg(name_ms="nf" + str(i + 3),
                                                      id_ms=i + 3,
                                                      space=mem_seg[idx].x1 - 50,
                                                      x1=50,
                                                      x2=mem_seg[idx].x1)
                                    mem_seg_f.append(segment)
                            else:
                                # if the segment is in the middle/OK
                                if mem_seg[idx].x1 > mem_seg[idx - 1].x2:
                                    segment_m = Mem_Seg(name_ms="nf" + str(i + 3),
                                                        id_ms=i + 3,
                                                        space=mem_seg[idx].x1 - mem_seg[idx - 1].x2,
                                                        x1=mem_seg[idx - 1].x2,
                                                        x2=mem_seg[idx].x1)
                                    mem_seg_f.append(segment_m)
                                # if it is the last segment
                                if idx == len(mem_seg) - 1:
                                    if mem_seg[idx].x2 != 800:
                                        segment = Mem_Seg(name_ms="nf" + str(i + 3),
                                                          id_ms=i + 3,
                                                          space=800 - mem_seg[idx].x2,
                                                          x1=mem_seg[idx].x2,
                                                          x2=800)
                                        mem_seg_f.append(segment)

            # change process quantity
            canvas.itemconfig(proc_num, text=str(len(list_p)))

            # create representation of memory to allocate
            rect_memo_piece = canvas.create_rectangle(355, 120, 355 + list_p[p].size, 170, fill='green',
                                                      outline="black")
            worst_idx = -1
            for seg_idx in range(len(mem_seg_f)):
                print("TAMANHO DA LISTA DE SEGMENTOS: ", len(mem_seg_f))
                # create rectangle to indicate free spaces
                rect_indicator = canvas.create_rectangle(mem_seg_f[seg_idx].x1, 20, mem_seg_f[seg_idx].x2, 70,
                                                         outline='red')
                # update canvas
                canvas.update()

                time.sleep(0.5)

                # check if actual segment has free space
                if mem_seg_f[seg_idx].space >= list_p[p].size:

                    # check if its the first one and set as worst idx
                    if worst_idx == -1:
                        worst_idx = seg_idx
                        # check if actual segment is bigger
                    elif mem_seg_f[worst_idx].space < mem_seg_f[seg_idx].space:
                        worst_idx = seg_idx

                canvas.delete(rect_indicator)

                # update canvas
                canvas.update()

                time.sleep(0.3)

                if seg_idx == len(mem_seg_f) - 1:
                    # delete segment representation
                    canvas.delete(rect_memo_piece)

                    # update screen
                    canvas.update()

                    # make smaller space in segment
                    mem_seg_f[worst_idx].space = mem_seg_f[worst_idx].space - list_p[p].size

                    # representation inside memory rectangle
                    rect_mem = canvas.create_rectangle(mem_seg_f[worst_idx].x1, 20,
                                                       mem_seg_f[worst_idx].x1 + list_p[p].size,
                                                       70, fill='green', tag=str(list_p[p].name))

                    # update screen
                    canvas.update()

                    # slower to see processes
                    time.sleep(0.3)

                    # variable to allocate segment
                    seg_atual = Mem_Seg(name_ms=list_p[p].name,
                                        id_ms=0,
                                        space=list_p[p].size,
                                        x1=mem_seg_f[worst_idx].x1,
                                        x2=mem_seg_f[worst_idx].x1 + list_p[p].size)

                    # put variable into segment list
                    mem_seg.append(seg_atual)

                    # sort segment list by x1 parameter
                    mem_seg.sort(key=lambda x: x.x1, reverse=False)

                    # generate new list of free segments
                    # generating new segments
                    mem_seg_f = []
                    for idx in range(len(mem_seg)):
                        # verify if it is the first occupied segment/OK
                        if idx == 0:
                            if mem_seg[idx].x1 > 50:
                                segment = Mem_Seg(name_ms="nf" + str(i + 3),
                                                  id_ms=i + 3,
                                                  space=mem_seg[idx].x1 - 50,
                                                  x1=50,
                                                  x2=mem_seg[idx].x1)
                                mem_seg_f.append(segment)
                        else:
                            # if the segment is in the middle/OK
                            if mem_seg[idx].x1 > mem_seg[idx - 1].x2:
                                segment_m = Mem_Seg(name_ms="nf" + str(i + 3),
                                                    id_ms=i + 3,
                                                    space=mem_seg[idx].x1 - mem_seg[idx - 1].x2,
                                                    x1=mem_seg[idx - 1].x2,
                                                    x2=mem_seg[idx].x1)
                                mem_seg_f.append(segment_m)
                            # if it is the last segment
                            if idx == len(mem_seg) - 1:
                                if mem_seg[idx].x2 != 800:
                                    segment = Mem_Seg(name_ms="nf" + str(i + 3),
                                                      id_ms=i + 3,
                                                      space=800 - mem_seg[idx].x2,
                                                      x1=mem_seg[idx].x2,
                                                      x2=800)
                                    mem_seg_f.append(segment)

                    wait_list.append(list_p[p])
                    # canvas.delete(rect_indicator)
                    list_p.remove(list_p[p])
                    delete_p = True
                    # p += 1
                    i -= 1
                    print("INDEX DO PROCESSO: ", str(p))
                    canvas.update()

            if delete_p == False:
                # remove o processo da lista de processos
                list_p.remove(list_p[p])
            # p += 1
            i -= 1
            print("INDEX DO PROCESSO: ", str(p))
            print("QTDE DE PROCESSOS: ", len(list_p))
            canvas.update()
            # refresh rate is 1 second
            time.sleep(1)