from datetime import timedelta

def input_yn(yes='y',no='n',alt_yes=[],alt_no=[],prompt='',bad_input_msg=None):   #retorna True o False
    alt_yes.append(yes)
    alt_no.append(no)
    if bad_input_msg==None:
        bad_input_msg='Type '+yes+' (yes) or '+no+' (no)\n'
    while True:
        flag=input(prompt+'['+ yes+'/'+no']: ')
        if flag in alt_yes:
            return True
        elif flag in alt_no:
            return False
        else:
            print(bad_input_msg)
    
def format_time(seconds):
    delta_t = timedelta(seconds=seconds)
    days = delta_t.days
    hours, remainder = divmod(delta_t.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    components = []
    if days:
        components.append(f"{days}D")
    if hours:
        components.append(f"{hours}H")
    if minutes:
        components.append(f"{minutes}M")
    if seconds:
        components.append(f"{seconds}S")

    time_string = " ".join(components)
    return time_string