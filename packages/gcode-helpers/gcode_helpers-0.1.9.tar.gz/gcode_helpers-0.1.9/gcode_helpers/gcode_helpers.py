import re 
import warnings

'''regex's'''
re_accel = re.compile('G65 F(\d+)')
re_decel = re.compile('G66 F(\d+)')

'''Getters'''
def get_accel_decel(line, accel=None, decel=None):

    # re_accel = re.compile('G65 F(\d+)')
    m = re_accel.match(line)

    if m is None:
        A = accel
    else:
        A = float(m.groups()[0])

    # re_decel = re.compile('G66 F(\d+)')
    m = re_decel.match(line)
    
    if m is None:
        D = decel
    else:
        D = float(m.groups()[0])

    return A, D

def get_print_mode(line, rel_mode):
    if 'G91' in line:
        rel_mode = True
    elif 'G90' in line:
        rel_mode = False

    return rel_mode

def get_pressure_config(line, p, com_port):
    
    regex = re.compile('Call setPress P(\d+) Q([0-9]+([.][0-9]*)?|[.][0-9]+)')
    m = regex.match(line)
    
    if m is None:
        return p, com_port
    else:
        return float(m.groups()[1]), int(m.groups()[0])

def are_we_printing(line, prev_printing_state, extrude_cmd=None, extrude_stop_cmd=None):
    # if nothing is provided, assume nordson pressure system
    if extrude_cmd is None:
        regex = re.compile('Call togglePress P(\d+)')
        m = regex.match(line)
        if m is None:
            return prev_printing_state
        else:
            return not prev_printing_state 
    
    else:
        if extrude_stop_cmd is None:
            extrude_stop_cmd = extrude_cmd
        # if only string is provided --> i.e., single extruding source
        if isinstance(extrude_cmd, str):
            if extrude_cmd.strip() in line:
                return True
            elif extrude_stop_cmd.strip() in line:
                return False
        
        # if using multimaterial printing or controlling multiple inputs
        elif hasattr(extrude_cmd, '__iter__'):
            # print(line)
            for start_cmd, stop_cmd in zip(extrude_cmd, extrude_stop_cmd):
                if stop_cmd.strip() in line:
                    prev_printing_state[start_cmd] = False
                    print('\tMM stopping = ', prev_printing_state)
                elif start_cmd.strip() in line:
                    prev_printing_state[start_cmd] = True
                    print('\tMM printing = ', prev_printing_state)
            
            # updated printing state
            return prev_printing_state
        else:
            raise ValueError('extrude_cmd must be a string or iterable (list, tuple) of strings')

def get_xyz(line):
    # X-COORDINATE
    s = re.search('X([+-]?\d+(\.\d+)?)', line)
    X = float(s.groups()[0]) if s is not None else None

    # Y-COORDINATE
    s = re.search('Y([+-]?\d+(\.\d+)?)', line)
    Y = float(s.groups()[0]) if s is not None else None

    # Z-COORDINATE
    s = re.search('Z([+-]?\d+(\.\d+)?)', line)
    Z = float(s.groups()[0]) if s is not None else None
    
    return X, Y, Z

def get_print_move(line, prev_move):
    # X-COORDINATE
    s = re.search('X([+-]?\d+(\.\d+)?)', line)
    X = float(s.groups()[0]) if s is not None else prev_move['COORDS'][0]

    # Y-COORDINATE
    s = re.search('Y([+-]?\d+(\.\d+)?)', line)
    Y = float(s.groups()[0]) if s is not None else prev_move['COORDS'][1]

    # Z-COORDINATE
    s = re.search('Z([+-]?\d+(\.\d+)?)', line)
    Z = float(s.groups()[0]) if s is not None else prev_move['COORDS'][2]
    
    # PRINT_SPEED
    s = re.search('F([+-]?\d+(\.\d+)?)', line)
    if s is not None:
        PRINT_SPEED = float(s.groups()[0])
    else:
        PRINT_SPEED = prev_move['PRINT_SPEED']

    if (X is None) and (Y is None) and (Z is None):
        return None, PRINT_SPEED
    else:
        return (X,Y,Z), PRINT_SPEED

'''SETTERS'''
def set_accel(line, accel):
    # Use regex to find the pattern "G65 F" followed by digits
    match = re.search(r'G65 F(\d+)', line)

    if match:
        # Match found
        line = f'G65 F{accel}' + '; acceleration mm/s^2 (modified)' + '\n'

    return line

def set_decel(line, decel):
    # Use regex to find the pattern "G66 F" followed by digits
    match = re.search(r'G66 F(\d+)', line)

    if match:
        # Match found
        line = f'G66 F{decel}' + '; deceleration mm/s^2 (modified)' + '\n'

    return line

def insert_after_line(lines, pattern, line_to_insert, insert_at_top=False):
    '''
        Args:
            lines (list): list of gcode lines
            pattern (str): regex pattern to do a line-by-line search
            line_to_insert (str): will insert `line_to_insert` after last occurence of `pattern`
        Returns:
            returns updated lines
    '''
    idxs = []

    for j, line in enumerate(lines):
        s = re.search(pattern, line)
        if s is not None:
            idxs.append(j)


    if len(idxs) > 0:
        idx = idxs[-1]

        print(idx)

        lines.insert(idx+1, line_to_insert)
    else:
        warnings.warn(f'>>> the pattern ({pattern}) did not find a match. So the line `{line_to_insert}` was inserted at the top.')
        if insert_at_top:
            lines.insert(0, line_to_insert)

    return lines
    






