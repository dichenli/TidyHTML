#CIT 591 Assignment 4
#Dichen Li and Siyang Shu

#Tidy HTML

import Tkinter
import tkFileDialog
import random
import sys
import os
##from tag_functions import *

 
def main():

    input_file = open_file()
    if input_file == None:
        return None
    input_name = input_file.name
    print input_name
    str_whole_file = read_file(input_file)
##    assert '<!DOCTYPE html>' in str_whole_file
    #File read in steps
    words_list = separate_out_strings(str_whole_file)
    #generate a words_list that stores all strings of the file by separating tags from other texts
    words_list = process_words_list(words_list)
    #do the majority of html formatting jobs  
    output_name = write_file(words_list)
    os.remove(input_name)
    os.rename(output_name, input_name)
    return

def open_file():
    """pop up a file open dialog to user to open an html file"""
    Tkinter.Tk().withdraw() # Close the root window
    in_path = tkFileDialog.askopenfilename()
    if (in_path[-5: -1] + in_path[-1]) != '.html':
        print "Error: input file does not have .html extension!"
        return None
    input_file = copy_input_file(in_path)
    return input_file    

def read_file(input_file):
    """Read the whole file, and store the text of file into a long string"""
    str_whole_file = input_file.read()
    input_file.close()
    return str_whole_file
    
def write_file(words_list):
    '''write a list of strings to file
    '''
    output_file = create_output_file()
    str_output = "".join(words_list)
    output_name = output_file.name
    for chars in str_output:
        output_file.write(chars)
    output_file.close()
    return output_name

def copy_input_file(filename):
    """for a given file name and directory,
    create a new file to work on with the same filename with extension .bak"""
    copyfile_name = filename + '.bak'
    original = open(filename, 'r')
    copy = open(copyfile_name, 'w')
    original_content = original.read()
    for chars in original_content:
        copy.write(chars) 
    original.close()
    copy.close() #close copy file here because it is used for writing, but we need the file for reading
    copy_read = open(copyfile_name, 'r') #open the copied file for reading purpose and return it
    return copy_read
    #http://www.tutorialspoint.com/python/file_methods.htm

#passed
def create_output_file():
    """Generate a name for the output file. The name should consist of a large random integer
    (use random.randint(1, sys.maxint)), with the .html extension."""
#return a file object as output file
    filename = str(random.randint(1, sys.maxint)) + '.html'
    output_file = open(filename, 'w')
    return output_file


def process_words_list(words_list):
    """do all formatting process of the html words list, return a words_list that looks tidy"""
    words_list = delete_empty_strings(words_list)
    words_list = check_nesting(words_list)
    words_list = delete_empty_strings(words_list)
    #correct wrong nestings
    words_list = lower_case_list(words_list)
    words_list = strip_whole_list(words_list)
    words_list = delete_empty_strings(words_list)
    #remove all empty spaces before and after each string, delete empty lines, then add new empty lines if needed
    words_list = generate_indentation(words_list)
    words_list = limit_lines_length(words_list, 80)
    words_list = strip_whole_list(words_list)
    words_list = generate_indentation(words_list)    
    words_list = delete_empty_strings(words_list)
    #indentations
    return words_list

#passed, independent function
def is_tag(tag_string):
    """return true if the string is a tag of any kind (start tag, end tag, empty_content_tag, pre_tag)"""
    string = str.strip(tag_string)
    if string == '':
        return False
    elif '<' in string[1: -1] or '>' in string[1: -1]:
    #consider case: '<a> blabla <\a>', it will not be judged as a tag given the condition above
        return False
##    elif string[-1] == '>' and string[0] == '<':
    elif string[0] == '<' and len(string) >= 2 and string[1].isalpha():
        return True
    elif string[0] == '<' and len(string) >= 3 and string[1] == '/' and string[2].isalpha():
        #<p>, <p dsf=dff21>, <h1 $$#%R%>, <br>, </br>, </br/> are all tags, but <//br> or <1 sdfds> are not
        return True
    return False

#passed, call: is_tag, retrieve_tag_name
def is_empty_content_tag(tag_string):
    """return true if it is an empty content tag"""
    if not is_tag(tag_string):
        return False
    tag_name = retrieve_tag_name(tag_string)
    empty_tags = ['area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img', 'input', 'isindex', 'link', 'meta', 'param']
    return tag_name in empty_tags


#passed, call: is_tag, retrieve_tag_name
def is_pre_tag(tag_string):
    """<pre>enclosed text</pre> Don't change the enclosed text in any way whatsoever; leave it exactly as is."""
    if not is_tag(tag_string):
        return False
    tag_name = retrieve_tag_name(tag_string)
    return tag_name == 'pre'

#passed
def is_pre_start_tag(tag_string):
    """return true if the string is <pre> or <pre XXXXXX>"""
    if not is_tag(tag_string):
        return False
    string = str.strip(tag_string)
    return string[0 : 4] == '<pre' and is_pre_tag(tag_string)

#passed
def is_pre_end_tag(tag_string):
    """return true if the string is </pre> or </pre XXXXXX>"""
    if not is_tag(tag_string):
        return False
    string = str.strip(tag_string)
    return string[0 : 5] == '</pre' and is_pre_tag(tag_string)

#passed, call: is_tag, retrieve_tag_name, is_empty_content_tag, is_pre_tag
def is_start_tag(tag_string):
    """Return true if it is an start tag, no matter whether it's <pre> or not"""
    string = str.strip(tag_string)
    if not is_tag(string):#To return true, it must be a tag, but not an end tag, or empty content tag.
        return False
##    elif is_pre_tag(string):
##        return False
    elif is_empty_content_tag(string):
        return False
    elif string[1].isalpha(): #probably end tag
        return True
    else:
        return False

#passed, call: is_tag, retrieve_tag_name, is_empty_content_tag, is_pre_tag
def is_end_tag(tag_string):
    """Return true if it is an end tag, no matter whether it's </pre> or not"""
    string = str.strip(tag_string)
    if not is_tag(string):#To return true, it must be a tag, but not an end tag, or empty content tag.
        return False
##    elif is_pre_tag(string):
##        return False
    elif is_empty_content_tag(string):
        return False    
    elif string[1] == '/' and string[2].isalpha():
        return True
    else:
        return False

#passed, call: is_tag
def retrieve_tag_name(tag_string):
    """give a string of complete tag in the form <...>, it returns the tag name.
    A string that is not a tag string is illegal.
    This function converts all upper case letters in tag name to lower case,
    but doesn't change the corresponding value in original data"""
    assert is_tag(tag_string)
    tagstring = str.strip(tag_string) #this function will still work for input such as'\n </a>\n\t'
    # we use a different variable here in case the original string is rewritten somehow
    tagname = ''
    if tagstring[1] == '/': #</hr>: will read from 'h', not '/'
        i = 2
    else:
        i = 1 #now tagstring[i] should be at the start of the tag name
    while i <len(tagstring) and (not tagstring[i] in [' ', '\t', '>', '\n', '/']):
    #<hr> <hr /> or <hr/> will retrieve 'hr' as tag name
    #i <len(tagstring) is just for safe proof
        tagname = tagname + tagstring[i]
        i += 1
    return tagname.lower()

def lower_case_tags(tag_string):
    """Given a tag_string, it change the upper cases in tag names to lower cases"""
    assert is_tag(tag_string)
    new_tag = ''
    i = 0
    while not tag_string[i].isalpha(): #before start of tagname
        new_tag = new_tag + tag_string[i]
        i += 1
    while tag_string[i] not in [' ', '\t', '>', '\n', '/']: #stops when tag name ends
        new_tag = new_tag + tag_string[i].lower()
        i += 1
    while i <len(tag_string):
        new_tag = new_tag + tag_string[i]
        i += 1
    return new_tag
        
        

#passed, call: is_tag, retrieve_tag_name, is_empty_content_tag, is_start_tag, is_end_tag
def tag_match(start_tag, end_tag):
    """it matchs start tag with end tag. start tag must be the first variable"""
    if not (is_start_tag(start_tag) and is_end_tag(end_tag)):
        return False
    return retrieve_tag_name(start_tag) == retrieve_tag_name(end_tag)

#passed
def create_end_tag(start_tag):
    """given a start tag string, return an end tag string that matches the start tag"""
    assert is_start_tag(start_tag)
    tag_name = retrieve_tag_name(start_tag)
    return '</' + tag_name + '>'

#passed
def find_end_tag_in_list(input_list, index):
    """for any input list of strings and an index that points to a start tag string,
    this function returns the end tag that match it. If no match is found, it returns None
    It also considers nesting. So for ['<a>', '<a>', '</a>'],
    find_end_tag_in_list(['<a>', '<a>', '</a>'], 0) returns None"""
    if not is_start_tag(input_list[index]): #The tag must be a start tag before it could have an end tag
        return None
    tag_name = retrieve_tag_name(input_list[index])
    i = index + 1
    while i < len(input_list):
        if is_tag(input_list[i]):
            if tag_name == retrieve_tag_name(input_list[i]):
            #There are two possibilities when the start tag name is equal to the tag name we find here
            #can't use tag_match() here. We want to also find two start tags that has the same name
                if is_start_tag(input_list[i]):
                #encounters nesting of the same start tag, for example: '<a>', '<a>', '</a>', '</a>'
                    i = find_end_tag_in_list(input_list, i)
                    #recursive call, returns the end tag index, then i++ below to jump over this end tag
                    if i == None:
                    #in case no end tag is found for the nesting start tag, for example:'<a>', '<a>'
                        return None
                elif is_end_tag(input_list[i]):
                #we find a matching end tag!!
                    return i #input_list[i] 
        i += 1
    return None #not found

##Test cases:
##has_end_tag_in_line(['<a>', '<b>', '<c>', 'a', '<c>', 's\n','s','s\n','s','s\n','s','<c>', '<c>', 's\n','s','s\n','s','s\n','s','s\n','s','<c>', '', '\n','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s\n','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s','s', '</c>', 'a', '</c>','</c>','</c>',' f\t', '</c>', '</b>', 's\n','s','s\n','s','s\n','s','d\n', '</a>'], 2)
##True
##has_end_tag_in_line(['<a>', '<b>', '<c>', 'a', '<c>', '<c>', '<c>', '<c>', '', '</c>', 'a', '</c>','</c>','</c>',' f\t', '</c>', '</b>', 'd\n', '</a>'], 2)
##False


#passed
def has_newline(string_list):
    """This function tells whether the given string list has a '\n' """
    for string in string_list:
        if '\n' in string:
            return True
    return False


#passed
def has_end_tag_in_same_line(input_list, index):
    """Give a list that stores the strings and an index that points to a tag,
    this function returns whether the end tag is in the same line as the start tag"""
#inputfile_list: a very long list of strings that saves all components of input file
    end_index = find_end_tag_in_list(input_list, index)
    return not has_newline(input_list[index : end_index])



def generate_indentation(words_list):
    '''words_list is a list of strings. generate proper indentation at proper places'''
    i = 0
    indentation = 0
##    check_newline_position(words_list)
##    str_temp = " "
    while(i < len(words_list)):
        if is_end_tag(words_list[i]):
            indentation -= 2
            if i > 0 and words_list[i-1][-1] != '\n': #end tag should be on a new line 
                words_list[i-1] = words_list[i-1] + '\n' #add '\n' to the previous string
        if is_start_tag(words_list[i]) and i > 0 and words_list[i-1][-1] != '\n': #start tag is not at the first of line:
        #by the way, no worry that this start tag is inside a one-line tag pair, it will be overlooked as is shown below
            words_list[i-1] = words_list[i-1] + '\n' #add '\n' to the previous string
        if i > 0 and words_list[i-1][-1] == '\n' and words_list[i] != '\n': #at head of line, not empty line
            words_list[i] = " " * indentation + str.lstrip(words_list[i])

        if is_pre_start_tag(words_list[i]): #if we find <pre>
            i = find_end_tag_in_list(words_list, i) #we will overlook the whole segment until after </pre>
        if is_start_tag(words_list[i]) and has_end_tag_in_same_line(words_list, i): #if end tag is in the same line
            i = find_end_tag_in_list(words_list, i)#we will overlook the whole segment until after the end tag
        elif is_start_tag(words_list[i]):
        #if it is a start tag, but end tag is not on the same line, then increase indentation from next line on
            indentation += 2
        i += 1
    indentation = 0
    return words_list

def replace_space(str):
    '''replace all spaces in the head of a string
    '''
    i = 0
    while(i < len(str)):
        if(str[i] == ' '):
            str = str[1:]
        else:
            return str
    return ""


def delete_empty_strings(input_list):
    """go through the whole list, find all strings that are '', delete them"""
    i = 0
    while i < len(input_list):
        if input_list[i] == '':
            del input_list[i]
            continue
        i += 1
    return input_list

def lower_case_tag(tag_string):
    """Given a tag_string, it change the upper cases in tag names to lower cases"""
    assert is_tag(tag_string)
    new_tag = ''
    i = 0
    while not tag_string[i].isalpha(): #before start of tagname
        new_tag = new_tag + tag_string[i]
        i += 1
    while tag_string[i] not in [' ', '\t', '>', '\n', '/']: #stops when tag name ends
        new_tag = new_tag + tag_string[i].lower()
        i += 1
    while i <len(tag_string):
        new_tag = new_tag + tag_string[i]
        i += 1
    return new_tag

def lower_case_list(input_list):
    """go through the whole list, find all upper case tags and replace by lower cases"""
    i = 0
    while i < len(input_list):
        if is_tag(input_list[i]):
            input_list[i] = lower_case_tag(input_list[i])
        i += 1
    return input_list

#passed
def separate_out_strings(str):
    '''break a string to a list of string in which there are tags and plain texts
    '''
    i = 0
    j1= j2 = 0
    words_return = []
    str_len = len(str)
    while(i < str_len):
        if(str[i] != '<' and str[i] != '>' and str[i] != '\n'):
            i += 1
            continue
        elif(i + 4 < len(str) and str[i : i + 4] == '<!--'): #if find start of note sign
            i = i + 4 #starts from the char following <!--
            while i + 3 <= len(str) and str[i : i + 3] != '-->': #until we find end of note sign
                i += 1
            i += 2 # now index points to the end of the note sign '>'
        elif i + 2 < len(str) and is_tag(str[i:i+3]): #is start of tag
            j2 = i
        elif str[i] == '>' and is_tag(str[j1:j1+3]): #is end of tag
            # print str[j1:j1+3]
            j2 = i + 1
        elif(str[i] == '\n'):
            j2 = i + 1
        if(j1 < j2):
            words_return.append(str[j1:j2])
            j1 = j2
        i += 1
    if(j1 < i):
        words_return.append(str[j1:i])
    return words_return



#passed
def need_to_insert_empty_line(tag_string):
    """There should be exactly one blank line before each of the following start tags:
    head, body, h1, h2, h3, h4, h5, h6"""
    if is_start_tag(tag_string):
        tag_name = retrieve_tag_name(tag_string)
        if tag_name in ['head', 'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            return True
    return False



def insert_empty_line(input_list, index):
    """if need to insert empty line, as is shown above, insert it."""
    assert need_to_insert_empty_line(input_list[index])
    if index > 0 and input_list[index - 1] != '' and input_list[index - 1][-1] != '\n':
        input_list[index - 1] = input_list[index - 1] + '\n'
    input_list.insert(index, '\n')
    return input_list


#passed
def string_strip(string):
    """This function removes all empty spaces, '\t' and '\n' before and after one string.
    Then if the original string has at least one '\n' in the end, put exactly one '\n' back"""
    i = len(string) - 1
    if i < 0:
        return string
    newline = '' #newline tells whether there is a '\n' at the end of string 
    while i >= 0 and string[i] in [' ', '\t']:
        i -= 1
    if string[i] == '\n':
        newline = '\n'
    string = str.strip(string) + newline
    return string

#passed
def strip_whole_list(input_list):
    """This function run string_strip function to every string in the input string list
    if an empty line is discovered, it also deletes the empty lines, and insert empty lines when needed"""
    i = 0
    while i < len(input_list):
        # print input_list[i]
        input_list[i] = string_strip(input_list[i])
        if input_list[i] == '':
            del input_list[i]
            continue
        if is_pre_start_tag(input_list[i]): #exception on pre tag
            input_list[i] = str.lstrip(input_list[i])
            i = find_end_tag_in_list(input_list, i)
            input_list[i] = str.rstrip(input_list[i])
        if input_list[i] == '\n':
            if i == 0 or input_list[i - 1][-1] == '\n': #the if judgements here try to find out an empty line
            #i==0 is the exception when the first string is '\n'
                del input_list[i]
                continue
        if need_to_insert_empty_line(input_list[i]):
            input_list = insert_empty_line(input_list, i)
            i += 2
        else:
            i += 1
    return input_list



def frozen_pre_strings(words_list):
    """for a given words_list, this function finds the elements that are between <pre> tags, label them as 'not changable'"""
    i = 0
    frozen_strings = []
    while i < len(words_list):
        if is_pre_start_tag(words_list[i]):
            end_index = find_end_tag_in_list(words_list, i)
            while i < end_index:
                frozen_strings.append(i)
                i += 1
        i += 1
    return frozen_strings


#passed
def make_cut(words_list, i, j):
    """do the cut at the given point,inserts a '\n' at the point right on the left of the cut point,
    and split the string to two strings, then strip two sides of the new strings to remove any empty spaces left"""
    right_half = str.lstrip(words_list[i][j : len(words_list[i])])
    if right_half != '':
        words_list.insert(i + 1, right_half)
    words_list[i] = str.rstrip(words_list[i][0 : j]) + '\n'
    #inserts a '\n' at the point right on the left of the cut point, and split the string to two strings
    #then strip two sides of the new strings to remove any empty spaces left
    return (words_list, i + 1) #cut successful, so return the point of new line    

#passed
def cut_line_left(words_list, cut_index, cut_point, frozen_strings):
    """For any given cut_point index on a words list (to the exact char index),
    it trys to find the first empty space on its left and insert a '\n'."""
    i = cut_index
    j = cut_point
    while i >= 0:
        if i not in frozen_strings: #we don't cut strings protected by <pre>
            while j >= 0:
                if words_list[i][j] in ['\t',' ']:
                    return make_cut(words_list, i, j) #cut successful, so return the point of new line
                elif words_list[i][j] == '\n':
                    #if no proper cut point can be found, then return to start point and try to cut on right
                    return cut_line_right(words_list, cut_index, cut_point, frozen_strings)
                j -= 1
        i -= 1
        j = len(words_list[i]) - 1
    return cut_line_right(words_list, cut_index, cut_point, frozen_strings)

#passed
def cut_line_right(words_list, cut_index, cut_point, frozen_strings):                
    """For any given cut_point index on a words list (to the exact char index),
    it trys to find the first empty space on its right and insert a '\n'."""
    i = cut_index
    j = cut_point
    while i < len(words_list):
        if i not in frozen_strings:
            while j < len(words_list[i]):
                if words_list[i][j] in ['\t',' ']:
                    return make_cut(words_list, i, j) #cut successful, so return the point of new line
                elif words_list[i][j] == '\n':
                    #if no proper cut point can be found, then return the string from the next line
                    return (words_list, i + 1)
                j += 1
        i += 1
        j = 0
    return (words_list, i + 1)


def limit_lines_length(words_list, max_length):
    """for an input list that stores all the input strings,
    this method test the length of each line, if > 80, it cuts the line to two"""
    frozen_strings = frozen_pre_strings(words_list)
    i = 0
    while i < len(words_list):
        line_length = find_line_length(words_list, i)
        if line_length <= max_length:
            i += 1
        else:
            while find_line_length(words_list, i) > max_length:
                (cut_index, cut_point) = find_index_at_length(words_list, i, max_length)
                assert cut_index != None #check that start position for cutting is found
                (words_list, i) = cut_line_left(words_list, cut_index, cut_point, frozen_strings)
    return words_list
            
        
    
def find_line_length(words_list, index):
    """For any word_list and a starting point of searching (first char of the words_list[index])
    this function returns the length of the current line starting from this point, and the index where the line ends"""
    line_length = 0
    i = index
    if i > 0 and '\n' in words_list[i - 1]:
        line_length += (len(words_list[i-1]) - words_list[i - 1].index('\n') - 1)
        # if a '\n' is in the middle of a string, find the part of the string after the '\n' on the same line
    while i < len(words_list):
        if '\n' in words_list[i]:
            line_length += words_list[i].index('\n') #the position of '\n' in the string
            break
        line_length += len(words_list[i])
        i += 1
    return line_length


#passed
def find_index_at_length(words_list, index, set_length):
    """given a start point index in the words list, and a given set_length,
    this function returns the end point index as words_list[i][remain_length]
    at which the string length reaches set_length"""
    #WARNING: this function don't care whether a '\n' is counted
    i = index
    remain_length = set_length 
    while i < len(words_list):
        if len(words_list[i]) >= remain_length:
            break
        remain_length -= len(words_list[i])
        i += 1
    if i >= len(words_list):
        return (None, None)
    return (i, remain_length - 1) # - 1 because arrays counts from 0
        

#passed
def check_nesting(input_list):
    """If an end tag (call it "E") doesn't match the last thing on the list of start tags,
    then insert an end tag for that start tag, and pop the start tag from the list.
    If E still doesn't match, do it again. If, after inserting two end tags,
    E still doesn't match the last thing in the list, discard E. """
    i = 0
    fix_count = 0
    tag_stack = []
    while i < len(input_list):
        if is_start_tag(input_list[i]): # push onto stack 
            tag_stack.append(input_list[i])
        elif is_end_tag(input_list[i]): #meet end tag
            if tag_stack != [] and tag_match(tag_stack[-1], input_list[i]):#tags match
                tag_stack.pop()# pop out of stack if match
                if fix_count > 0:
                    #after the fix below, things match now. So fix count is now used for the next tag
                    fix_count = 0
            elif tag_stack == []:
                #stack is empty, so there is an extra end tag by mistake
                del input_list[i]
                continue #one element is deleted, so index -1, no need for i++ in this loop
            elif tag_stack != [] and fix_count <= 2: #stack is not empty but tags don't match
                input_list.insert(i, create_end_tag(tag_stack.pop()))
                #create and insert an end tag that matches the start tag
                #be aware that after insertion, all the indexes will increase by 1
                fix_count += 1
            else:
                #Two possibilities here that lead to the same solution:
                #First, tag_stack is empty, so there is an extra end tag by mistake, delete it
                #Second, we've tried to add aditional tags twice, they still don't match, so just delete!
                del input_list[i]
                continue #one element is deleted, so index -1, no need for i++ in this loop
        i += 1
    while tag_stack != []:
        input_list.append(create_end_tag(tag_stack.pop())) #Finally, if tag stack is not empty, just add end tags
    return input_list

"""we should check nesting first before we do anything else to process the input list!!"""
##test cases:
##>>> check_nesting(['<a>','<b>','<c>','<d>','<e>','<f>','<g>','<h>','<i>','</h>','</i>','</g>','</f>','</e>','</d>','</c>','</b>','</a>'])
##['<a>', '<b>', '<c>', '<d>', '<e>', '<f>', '<g>', '<h>', '<i>', '</i>', '</h>', '</g>', '</f>', '</e>', '</d>', '</c>', '</b>', '</a>']
##>>> check_nesting(['<a>','1','<b>','2','<c>','3','</c>','4','</b>','5','</a>'])
##['<a>', '1', '<b>', '2', '<c>', '3', '</c>', '4', '</b>', '5', '</a>']
##>>> check_nesting(['<a>','1','<b>','2','<c>','3','</b>','4','</c>','5','</a>'])
##['<a>', '1', '<b>', '2', '<c>', '3', '</c>', '</b>', '4', '</a>', '5']
##>>> check_nesting(['<a>','1','<b>','2','<c>','3','</c>','4','5','</a>'])
##['<a>', '1', '<b>', '2', '<c>', '3', '</c>', '4', '5', '</b>', '</a>']
##>>> check_nesting(['<a>','1','<b>','2','<c>','3','<d>','4','</a>'])
##['<a>', '1', '<b>', '2', '<c>', '3', '<d>', '4', '</d>', '</c>', '</b>', '</a>']








###dead code
###passed
##def combine_pre_segment(input_list, start_index):
##    """This function combines all contents between '<pre>' and matching '<pre>' as one single string.
##    input_list is the list of strings. index is the start index of the <pre> tag
##    For example, ['<pre>', '\n11\n\t a', '</pre>'] will be combined to ['<pre>\n11\n\t a</pre>']
##    As a result, it will no longer be processed anyhow"""
##    #WARNING: It will change the original input_list even without any return value
##    assert is_pre_start_tag(input_list[start_index])
##    end_index = find_end_tag_in_list(input_list, start_index)
##    i = end_index - start_index
##    #now starts combination. Append each following string to the '<pre>', then delete
##    while i > 0: 
##        input_list[start_index] = input_list[start_index] + input_list[start_index + 1]
##        del input_list[start_index + 1]
##        i -= 1
##    return input_list
####    # print input_list[start_index]
##
##
###dead code
###passed
##def exclude_pre_tags(input_list):
##    """This function travel through the whole list and calls combine_pre_segment every time it meets a <pre>"""
##    i = 0
##    while i < len(input_list):
##        if is_pre_start_tag(input_list[i]):
##            combine_pre_segment(input_list, i)
##        i += 1
##    return input_list
#passed


##def insert_newline_to_list(words_list, max_length):
##    """This function insert a '\n' to the list chars whenever it becomes longer than max_length characters"""
##    insert_index = [0, 0]
##    front_index = [0, 0]
##    i = 0
##    j = 0
##    length_count = 0
##    while i < len(words_list):
##        while j < len(words_list[i]):
##            if words_list[i][j] == '\n':
##                if length_count > max_length:
##                    words_list.insert(insert_index[0] + 1, words_list[insert_index[0]][insert_index[1]:-1])
##                    words_list[insert_index[0]] = words_list[insert_index[0]][0:insert_index[1]] + '\n' #insert '\n'
##                length_count = 0
##            if words_list[i][j] in [' ', '\t']:
##                insert_index = [i, j]

##def combine_pre_segment(input_list, start_index):
##    """This function combines all contents between '<pre>' and matching '<pre>' as one single string.
##    input_list is the list of strings. index is the start index of the <pre> tag
##    For example, ['<pre>', '\n11\n\t a', '</pre>'] will be combined to ['<pre>\n11\n\t a</pre>']
##    As a result, it will no longer be processed anyhow"""
##    #WARNING: It will change the original input_list even without any return value
##    assert is_pre_start_tag(input_list[start_index])
##    end_index = find_end_tag_in_list(input_list, start_index)
##    i = end_index - start_index
##    #now starts combination. Append each following string to the '<pre>', then delete
##    while i > 0: 
##        input_list[start_index] = input_list[start_index] + input_list[start_index + 1]
##        del input_list[start_index + 1]
##        i -= 1
####    # print input_list[start_index]
##
###passed

##def exclude_pre_tags(input_list):
##    """This function travel through the whole list and calls combine_pre_segment every time it meets a <pre>"""
##    i = 0
##    while i < len(input_list):
##        if is_pre_start_tag(input_list[i]):
##            combine_pre_segment(input_list, i)
##        i += 1
##    return input_list
##    
##def tidy_tags(words_list):
##    '''words_list is a list of strings which are tags or plain texts.
##    return a list of strings in which tags are all simplified (by simplify_tag function)
##    '''
##    i = 0
##    word = " "
##    while(i < len(words_list)):
##        if(is_tag(words_list[i])):
##            is_successful = False
##            j = i
##            while(not is_successful):
##                j += 1
##                (word, is_successful) = simplify_tag(" ".join(words_list[i:j]))
##            del words_list[i:j]
##            words_list.insert(i, word)
##        i += 1
##    return words_list


##def simplify_tag(str_input):
##    str = str_input.lower() #wrong
##    str = str.replace("\n", "")
##    str_list = str.split(" ")
##    i = 0
##    while(i < len(str_list)):
##        if(str_list[i] == ''):
##            del str_list[i]
##        else:
##            i += 1
##    str = " ".join(str_list)
##    if(str[-2] == ' '):
##        str = str[0:-2] + str[-1]
##    if(str[-1] == ">"):
##        return (str, True)
##    else:
##        return (str, False)

##def find_b_tag(words_list):
##    for string in words_list:
##        if is_tag(string) and retrieve_tag_name(string) == 'b':
##            #print string


       
if __name__ == "__main__":
    main()

