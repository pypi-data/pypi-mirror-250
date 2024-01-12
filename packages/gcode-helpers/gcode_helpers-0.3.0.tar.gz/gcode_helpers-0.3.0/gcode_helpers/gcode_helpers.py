import re
import numpy as np
import warnings
import copy

'''regex's'''
re_accel = re.compile('G65 F(\d+)')
re_decel = re.compile('G66 F(\d+)')
def is_float(string):
    try:
        float_value = float(string)
        return True
    except ValueError:
        return False
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

def get_printing_state(line, extrude_cmd, vars):
    m1 = re.search(f'{extrude_cmd}' + r'\s+([^;\n]+)', line)

    if is_float(m1.group(1)):
        return float(m1.group(1))
    else:
        try:
            expression = m1.group(1)
            for variable, value in vars.items():
                expression = expression.replace(variable, str(value))
            
            return np.round(eval(expression), 6)
        
        except:
            raise ValueError

def are_we_printing(line, prev_printing_state, extrude_cmd=None, extrude_stop_cmd=None, vars={}):
    # if nothing is provided, assume nordson pressure system
    if extrude_cmd is None:
        extrude_cmd = 'Call togglePress'
    if extrude_stop_cmd is None:
            extrude_stop_cmd = extrude_cmd
        
    # if only string is provided --> i.e., single extruding source
    if extrude_cmd == 'Call togglePress':
        if extrude_cmd.strip() in line:
            return {extrude_cmd: {
                'printing': not prev_printing_state['printing'],
                'value': 0 if prev_printing_state[extrude_cmd]['printing'] is False else 1
                }}
        else:
            return prev_printing_state

    elif isinstance(extrude_cmd, str):
        # cmd NO, cmd_stop No --> 1st if statement above
        # cmd YES, cmd_stop NO --> else below (i.e., assuming toggle switch convention)
        # cmd YES, cmd_stop YES --> 1st elif below
        if extrude_cmd.strip() in line and extrude_cmd.strip() == extrude_stop_cmd.strip():
            return {extrude_cmd: {'printing': not prev_printing_state[extrude_cmd]['printing'],
                                  'value': 0 if prev_printing_state[extrude_cmd]['printing'] is False else 1}}
        elif extrude_stop_cmd.strip() in line:
            return {extrude_cmd: {'printing': False, 'value': 0}}
        elif extrude_cmd.strip() in line:
            return {extrude_cmd: {'printing': True, 'value': 1}}
        else:
            return prev_printing_state
    
    # if using multimaterial printing or controlling multiple inputs
    elif hasattr(extrude_cmd, '__iter__'):
        new_state = copy.deepcopy(prev_printing_state)
        for start_cmd, stop_cmd in zip(extrude_cmd, extrude_stop_cmd):
            if stop_cmd.strip() in line:
                new_state[start_cmd]['printing'] = False
                new_state[start_cmd]['value'] = 0

                # continue
            elif start_cmd.strip() in line:
                new_state[start_cmd]['printing'] = True
                new_state[start_cmd]['value'] = get_printing_state(line, start_cmd, vars)

                # continue
        return copy.deepcopy(new_state)
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

def evaluate_as_float(pattern, line, default_value, rel_mode, vars):
    s = re.search(pattern, line)
    if s is None:
        return 0 if rel_mode and rel_mode else default_value
    elif is_float(s.group(1)):
        return float(s.group(1).strip())
    else:
        try:
            expression = s.group(1).strip()
            for variable, value in vars.items():
                expression = expression.replace(variable, str(value))
            
            return np.round(eval(expression), 6)
        
        except:
            raise ValueError('Could not determine coordinate from the gcode line: ', line)

def get_print_move(line, prev_move, rel_mode, vars):
    # X-COORDINATE
    X = evaluate_as_float('X\s*([^XYZF;\s]*)', line, prev_move['COORDS'][0] if rel_mode else prev_move['CURRENT_POSITION']['X'], rel_mode, vars)

    # Y-COORDINATE
    Y = evaluate_as_float('Y\s*([^XYZF;\s]*)', line, prev_move['COORDS'][1] if rel_mode else prev_move['CURRENT_POSITION']['Y'], rel_mode, vars)

    # Z-COORDINATE
    Z = evaluate_as_float('Z\s*([^XYZF;\s]*)', line, prev_move['COORDS'][2] if rel_mode else prev_move['CURRENT_POSITION']['Z'], rel_mode, vars)
    
    # PRINT_SPEED
    PRINT_SPEED = evaluate_as_float('F\s*([^XYZF;\s]*)', line, prev_move['PRINT_SPEED'], None, vars)

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

        # print(idx)

        lines.insert(idx+1, line_to_insert)
    else:
        warnings.warn(f'>>> the pattern ({pattern}) did not find a match. So the line `{line_to_insert}` was inserted at the top.')
        if insert_at_top:
            lines.insert(0, line_to_insert)

    return lines
    






