import adi
import numpy as np
import pandas as pd

def comment_grid( f ):
    
    comments = f.get_comments()
    recs = f.records

    comment_list = list()
    comment_list.append( {"Comment":"None", "UnixTime":0} )
    for i in range( len(comments) ):
        T0 = recs[comments[i].record_id-1].record_time.rec_datetime.timestamp()
        comment_list.append( {"Comment":comments[i].text, "UnixTime":comments[i].time+T0} )

    comment_frame = pd.DataFrame(comment_list)
    unq_comments = np.unique( comment_frame["Comment"] )

    for some_comment in unq_comments:
        counter = 0
        
        for i in range(len(comment_frame)):
            if comment_frame["Comment"].iloc[i]==some_comment:
                if counter==0:
                    counter+=1
                else:
                    new_comment = comment_frame["Comment"].iloc[i] + f" ({counter})"
                    #comment_frame["Comment"].iloc[i] = new_comment
                    comment_frame.loc[i, "Comment"] = new_comment

                    counter+=1
            
    return comment_frame

def df_from_file( fpath ):

    # Load the file
    f = adi.read_file( fpath )

    channels = f.channel_names
    Nrecord = f.n_records

    temp_dict = dict()

    for i, chan in enumerate(channels):
        if i==0:
            temp_dict["BlockTime"]=list()
            temp_dict["UnixTime"]=list()

        temp_dict[chan] = list()
        y = f.get_channel_by_name(chan)
        for j in range(Nrecord):
            try:
                t, data = y.get_data(j+1,return_time=True)
            except:
                if i>0:
                    t = np.empty(len(temp_dict["UnixTime"][j]))
                    t[:] = np.nan

                    data = np.empty(len(temp_dict["UnixTime"][j]))
                    data[:] = np.nan

                else:
                    t, data = [np.nan], [np.nan]

            temp_dict[chan].append(data)

            if i==0:
                T0 = f.records[j].record_time.rec_datetime

                temp_dict["BlockTime"].append(t)
                temp_dict["UnixTime"].append(t+T0.timestamp())

    stack_dict = dict()
    for key in temp_dict:
        stack_dict[key] = np.hstack(temp_dict[key])

    stack_frame = pd.DataFrame(stack_dict)

    comment_frame = comment_grid(f)

    init_comment = pd.Series(np.array(["None" for i in range(len(stack_frame))]))
    for i in range(len(comment_frame)):
        Tcomment = comment_frame["UnixTime"].iloc[i]
        post_comment = stack_frame["UnixTime"]>Tcomment
        init_comment.loc[ post_comment ] = comment_frame["Comment"].iloc[i]

    stack_frame["Last Comment"] = init_comment

    return stack_frame
