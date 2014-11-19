## Dichen Li and Siyang Shu
import unittest
from tidyHTML import *


class TestTidyHTML(unittest.TestCase):

    def test_open_file(self):
        print '\ntest_open_file'
        pass

    def test_read_file(self):
        print '\ntest_read_file'
        pass
        
    def test_write_file(self):
        print '\ntest_write_file'
        pass

    def test_copy_input_file(self):
        print '\ntest_copy_input_file'
        pass

    def test_create_output_file(self):
        print '\ntest_create_output_file'
        pass

    def test_process_words_list(self):
        print '\ntest_process_words_list'
        pass

    def test_is_tag(self):
        print '\ntest_is_tag'
        self.assertEqual(False, is_tag('<'))
        self.assertEqual(False, is_tag('< a>'))
        self.assertEqual(True, is_tag('<h4>'))
        self.assertEqual(True, is_tag('<A\na>'))
        self.assertEqual(True, is_tag('<pre a>'))
        self.assertEqual(True, is_tag('</pre>'))
        self.assertEqual(True, is_tag('<b '))
        
    def test_is_empty_content_tag(self):
        print '\ntest_is_empty_content_tag'
        self.assertEqual(True, is_empty_content_tag('<area>'))
        self.assertEqual(True, is_empty_content_tag('<base >'))
        self.assertEqual(True, is_empty_content_tag('<basefont'))
        self.assertEqual(False, is_empty_content_tag('< area>'))
        self.assertEqual(False, is_empty_content_tag('<bas>'))
        
    def test_is_pre_tag(self):
        print '\ntest_is_pre_tag'
        self.assertEqual(True, is_pre_tag('<pre>'))
        self.assertEqual(True, is_pre_tag('<pre >'))
        self.assertEqual(True, is_pre_tag('</pre>'))
        self.assertEqual(False, is_pre_tag('<prea>'))
        self.assertEqual(False, is_pre_tag('pre>'))
        
    def test_is_pre_start_tag(self):
        print '\ntest_is_pre_start_tag'
        self.assertEqual(True, is_pre_start_tag('<pre>'))
        self.assertEqual(True, is_pre_start_tag('<pre\n>'))
        self.assertEqual(True, is_pre_start_tag('<pre '))
        self.assertEqual(False, is_pre_start_tag('<\pre>'))
        
    def test_is_pre_end_tag(self):
        print '\ntest_is_pre_end_tag'
        self.assertEqual(True, is_pre_end_tag('</pre>'))
        self.assertEqual(True, is_pre_end_tag('</pre\n>'))
        self.assertEqual(True, is_pre_end_tag('</pre '))
        self.assertEqual(False, is_pre_end_tag('<pre>'))
        self.assertEqual(False, is_pre_end_tag('!/pre>'))
        
    def test_is_start_tag(self):
        print '\ntest_is_start_tag'
        self.assertEqual(True, is_start_tag('<pre>'))
        self.assertEqual(True, is_start_tag('<h2>'))
        self.assertEqual(True, is_start_tag('<tag\n'))
        self.assertEqual(False, is_start_tag('</tag>'))
        self.assertEqual(False, is_start_tag('<base>'))
        
    def test_is_end_tag(self):
        print '\ntest_is_end_tag'
        self.assertEqual(True, is_end_tag('</pre>'))
        self.assertEqual(True, is_end_tag('</a>'))
        self.assertEqual(True, is_end_tag('</a sdf>'))
        self.assertEqual(False, is_end_tag('<tag>'))
        self.assertEqual(False, is_end_tag('</base>'))
        
    def test_retrieve_tag_name(self):
        print '\ntest_retrieve_tag_name'
        self.assertEqual('base', retrieve_tag_name('<base>'))
        self.assertEqual('pre', retrieve_tag_name('</pre aa>'))
        self.assertEqual('h1b', retrieve_tag_name('<h1b asd>'))
        self.assertEqual('b1', retrieve_tag_name('<b1/n'))
        self.assertEqual('what', retrieve_tag_name('<what tag'))
        
    def test_tag_match(self):
        print '\ntest_tag_match'
        self.assertEqual(False, tag_match('<base>','</base>'))
        self.assertEqual(True, tag_match('<pre>','</pre>'))
        self.assertEqual(False, tag_match('<a1>','<a1>'))
        self.assertEqual(True, tag_match('<tag','</tag>'))
        
    def test_create_end_tag(self):
        print '\ntest_create_end_tag'
        self.assertEqual('</pre>', create_end_tag('<pre>'))
        self.assertEqual('</good>', create_end_tag('<Good !!>'))
        self.assertEqual('</baseball>', create_end_tag('<BASEBALL\n>'))
        self.assertEqual('</tag>', create_end_tag('<Tag'))
        
    def test_find_end_tag_in_list(self):
        print '\ntest_find_end_tag_in_list'
        self.assertEqual(None, find_end_tag_in_list(['<a>', '<a>', '</a>'], 0))
        self.assertEqual(2, find_end_tag_in_list(['<a>', '<a>', '</a>'], 1))
        self.assertEqual(4, find_end_tag_in_list(['<a>', '<a','\n>aa', '</a>', '</a>'], 0))
        self.assertEqual(5, find_end_tag_in_list(['<a>', '<a>', '</a>', '<a>', '</a>', '</a>'], 0))
        
    def test_has_newline(self):
        print '\ntest_has_newline'
        self.assertEqual(True, has_newline(['<ba\nse>']))
        self.assertEqual(True, has_newline(['saf\n','ab \n']))
        self.assertEqual(False, has_newline(['ab \\n']))
        self.assertEqual(False, has_newline([]))
        self.assertEqual(False, has_newline([''])) 
        
    def test_has_end_tag_in_same_line(self):
        print '\ntest_has_end_tag_in_same_line'
        self.assertEqual(True, has_end_tag_in_same_line(['<good>', 'sdf', '</good>\n'], 0))
        self.assertEqual(False, has_end_tag_in_same_line(['<good>', 'sdf\n', '</good>'], 0))
        self.assertEqual(False, has_end_tag_in_same_line(['<good\n sfd>', 'sdf', '</good>\n'], 0))
        self.assertEqual(False, has_end_tag_in_same_line(['<base>', 'sdf', '</base>\n'], 0))
        self.assertEqual(False, has_end_tag_in_same_line(['<good>', 'sdf', '</good>'], 3))
        
    def test_generate_indentation(self):
        print '\ntest_generate_indentation'
        self.assertEqual(['<a>', 'aaa', '</a>'], generate_indentation(['<a>', 'aaa', '</a>']))
        self.assertEqual(['<a>\n', '  aaa\n', '</a>'], generate_indentation(['<a>\n', 'aaa', '</a>']))
        self.assertEqual(['<a>\n', '  <b>', 'aaa\n', '  </b>\n', '</a>'], generate_indentation(['<a>\n', '<b>','aaa\n', '</b>', '</a>']))
        self.assertEqual(['<p2>\n', '  <a href="aaaa";\n', '    title="aaaa">', 'aaaa\n', '  </a>\n', '  <b>', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', '</b>\n', '</p2>'], generate_indentation(['<p2>', '<a href="aaaa";\n', 'title="aaaa">', 'aaaa', '</a>', '<b>', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', '</b>', '</p2>']))
        
    def test_delete_empty_strings(self):
        print '\ntest_delete_empty_strings'
        self.assertEqual(['<a>', '</a>'], delete_empty_strings(['<a>', '', '</a>']))
        self.assertEqual([], delete_empty_strings(['']))
        self.assertEqual([], delete_empty_strings([]))

    def test_lower_case_tag(self):
        print '\ntest_lower_case_tags'
        self.assertEqual('<base>', lower_case_tag('<bASe>'))
        self.assertEqual('<base>', lower_case_tag('<base>'))
        self.assertEqual('<a2b A2B>', lower_case_tag('<A2B A2B>'))
        self.assertEqual('<what', lower_case_tag('<WHAT'))
        self.assertEqual('<pre\nbase>', lower_case_tag('<prE\nbase>'))
        
    def test_lower_case_list(self):
        print '\ntest_lower_case_list'
        self.assertEqual(['<good  AAA>', 'SSS', '</good>\n'], lower_case_list(['<GOOD  AAA>', 'SSS', '</GOod>\n']))
        self.assertEqual([''], lower_case_list(['']))
        self.assertEqual([], lower_case_list([]))
        
    def test_separate_out_strings(self):
        print '\ntest_separate_out_strings'
        self.assertEqual(['<p2>', ' ', '<a href="aaaa"; title="aaaa">', 'aaaa', '</a>', ' ', '<b>', 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', '</b>', ' ', '</p2>'], separate_out_strings('<p2> <a href="aaaa"; title="aaaa">aaaa</a> <b>bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb</b> </p2>'))
        self.assertEqual(['<p2>', ' ', '<a \n', 'aa>aa\n', 'aa', '</a>', ' ', '\n', '<b>', 'b', '</b>', ' ', '</p2>'], separate_out_strings('<p2> <a \naa>aa\naa</a> \n<b>b</b> </p2>'))
        self.assertEqual([], separate_out_strings(''))

    def test_need_to_insert_empty_line(self):
        print '\ntest_need_to_insert_empty_line'
        self.assertEqual(True, need_to_insert_empty_line('<h1>'))
        self.assertEqual(True, need_to_insert_empty_line('<hEAD'))
        self.assertEqual(False, need_to_insert_empty_line('<pre>'))
        self.assertEqual(False, need_to_insert_empty_line('<>'))
        
    def test_insert_empty_line(self):
        print '\ntest_insert_empty_line'
        self.assertEqual(['<head>\n', '\n', '<h1>', '<pre>', '</h1>', '<ab>', '</ab>', 'sdf', '\n'], insert_empty_line(['<head>','<h1>','<pre>','</h1>','<ab>','</ab>','sdf','\n'], 1))
        self.assertEqual(['\n', '<head>', '<h1>', '<pre>', '</h1>', '<ab>', '</ab>', 'sdf', '\n'], insert_empty_line(['<head>','<h1>','<pre>','</h1>','<ab>','</ab>','sdf','\n'], 0))

    def test_string_strip(self):
        print '\ntest_string_strip'
        self.assertEqual('<h1>', string_strip('<h1>'))
        self.assertEqual('<h1>\n', string_strip('<h1>\n\t'))
        self.assertEqual('s  a', string_strip('  \ts  a\t  '))
        self.assertEqual('s  a\n', string_strip('  \ts  a\n\t  '))
        self.assertEqual('s  a\n', string_strip('  \ts  a\t\n  '))
        
    def test_strip_whole_list(self):
        print '\ntest_strip_whole_list'
        self.assertEqual(['ab\n', '\n', '<h2>', 's  a\n', '<pre>', '  ', '</pre>', '\n', '<a>\n', '</a>'], strip_whole_list(['ab', '<h2>', '  \ts  a\t\n  ', '<pre>', '  ', '</pre>', '  \n', '<a>\n', '</a>']))
        self.assertEqual(['dsf\n', '\n', '<h1>', '</h1>\n', '<sd>\n', '\n', '<head>', '</head>', '\n', 'sd'], strip_whole_list(['dsf', '\t<h1>', '  </h1>\n\t ', '   <sd> \n', '<head>', '</head>', '\t\t\n\t ','  sd  ']))
        self.assertEqual(['\n', '<head>\n', '</head>', 'dsf', '</h1>\n', '<pre>\n', '<head>', '</head>', '\t\t\n\t ', '  </pre>'], strip_whole_list(['  <head>\n', '  </head>  ', 'dsf', '', '  </h1>\n\t ', '   <pre> \n', '<head>', '</head>', '\t\t\n\t ','  </pre>  ']))
        
    def test_frozen_pre_strings(self):
        print '\ntest_frozen_pre_strings'
        self.assertEqual([0, 1, 4, 5], frozen_pre_strings(['<pre>', '\n', '</pre>', 's  a', '<pre>', '  ', '</pre>', '<a>\n', '</a>']))
        self.assertEqual([], frozen_pre_strings(['<pr>', '\n', '</pr>', 's  a', '<pr>', '  ', '</pr>', '<a>\n', '</a>']))
        self.assertEqual([], frozen_pre_strings(['<pre>', '\n', '</pr>', 's  a', '<pr>', '  ', '</pr>', '<a>\n', '</a>']))
        self.assertEqual([0, 1, 2, 3, 4, 5], frozen_pre_strings(['<pre>', '\n', '</pr>', 's  a', '<pr>', '  ', '</pre>', '<a>\n', '</a>']))
        
    def test_make_cut(self):
        print '\ntest_make_cut'
        self.assertEqual((['\n', 's  a\t\n  ', 'as'], 1), make_cut(['  \ts  a\t\n  ', 'as'], 0, 2))
        self.assertEqual((['  \ts  a\t\n  ', 'as\n'], 2), make_cut(['  \ts  a\t\n  ', 'as'], 1, 2))
        self.assertEqual((['asd\ng\n', 'fds sdf  a\t\n  ', 'as'], 1), make_cut(['asd\ng  fds sdf  a\t\n  ', 'as'], 0, 7))
        
    def test_cut_line_left(self):
        print '\ntest_cut_line_left'
        self.assertEqual((['  \ts\n', 'a\t\n  ', 'as'], 1), cut_line_left(['  \ts  a\t\n  ', 'as'], 0, 6, []))
        self.assertEqual((['aaaaaaa\n', 'aa', 'as'], 1), cut_line_left(['aaaaaaa\t\naa', 'as'], 0, 7, []))
        self.assertEqual((['aaaaaaa\t\naa', 'as'], 3), cut_line_left(['aaaaaaa\t\naa', 'as'], 0, 7, [0]))
        self.assertEqual((['123', '45\n', '\n', '123', '45\n', '789', '123', '456', '789'], 3), cut_line_left(['123', '45\n', '\t','123', '45\n', '789','123', '456', '789'], 4, 1, []))
        
    def test_cut_line_right(self):           
        print '\ntest_cut_line_right'
        self.assertEqual((['  \ts  a\n', 'as'], 1), cut_line_right(['  \ts  a\t\n  ', 'as'], 0, 6, []))
        self.assertEqual((['aaaaaaa\t\naa', 'as'], 3), cut_line_right(['aaaaaaa\t\naa', 'as'], 0, 7, [0]))
        self.assertEqual((['aaaaaaa\t\naa', 'a\n', 's'], 2), cut_line_right(['aaaaaaa\t\naa', 'a s'], 0, 7, [0]))
        
    def test_limit_lines_length(self):
        print '\ntest_limit_lines_length'
        self.assertEqual(['123', '45\n', '\n', '<a1\n', '23>', '45\n', '7 89\n', '123\n', '4\n', '456\n', '12', '3\n', '4', '\n'] , limit_lines_length(['123', '45\n', '\t','<a1  23>', '45\n', '7 89\n','123 4\n', '456  \n', '12', '3 4', '\n'], 4))
        self.assertEqual(['123', '45\n', '<pre>\t', '<a1  23>', '4  e 5', '</pre>', 's\n', 'df\n', '7 89\n', '123\n', '4\n', '456\n', '12', '3\n', '4', '\n'] , limit_lines_length(['123', '45\n', '<pre>\t','<a1  23>', '4  e 5', '</pre>','s df\n', '7 89\n','123 4\n', '456  \n', '12', '3 4', '\n'], 4))
        self.assertEqual(['11111111111111111111111111111111111111111111111111111111\n', '111111111111111111111111111111111111111111111111111111\n', '1111111111111111111111111111111111111111', '<pre>', '1111111111111111111111\n', '11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', '<\\pre>', '123\n', '41111111111111111111111111111111111111\n', '456  \n', '12', '3 4', '\n'] , limit_lines_length(['11111111111111111111111111111111111111111111111111111111 111111111111111111111111111111111111111111111111111111 1111111111111111111111111111111111111111', '<pre>','1111111111111111111111  11111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', '<\pre>','123 41111111111111111111111111111111111111\n', '456  \n', '12', '3 4', '\n'], 20))
        
    def test_find_line_length(self):
        print '\ntest_find_line_length'
        self.assertEqual(11, find_line_length(['dsf', '\t<h1>', '  </h1>\n\t ', '   <pre> \n', '<head>', '</head>', '\t\t\n\t ','  </pre>  ','dsf\n', '\n', '<h1>', '</h1>\n', '<pre>\n', '<head>', '</head>', '\t\t\n\t ', '  </pre>'], 3))
        self.assertEqual(12, find_line_length(['dsf', '\t<h1>', '  </h1>\n\t ', '   <pre> \n', '<head>', '</head>', '\t\t\n\t ','  </pre>  ','dsf\n', '\n', '<h1>', '</h1>\n', '<pre>\n', '<head>', '</head>', '\t\t\n\t ', '  </pre>'], 1))
        self.assertEqual(5, find_line_length(['aaaaaaa\t\naa', 'a s'], 1))
        self.assertEqual(22, find_line_length(['<head>\n','\n','<h1>','<pre>','</h1>','<ab>','</ab>','sdf','\n'], 3))
              
    def test_find_index_at_length(self):
        print '\ntest_find_index_at_length'
        self.assertEqual((2, 1), find_index_at_length(['123', '456', '789', '0'], 1, 5))
        self.assertEqual((6, 2), find_index_at_length(['123', '456', '789','123', '456', '789','123', '456', '789'], 3, 12))
        self.assertEqual((None, None), find_index_at_length(['aaaaaaa\taa', 'aaaaaaaaaaaaaaaaaaaaaaaa\n'], 0, 80))
        self.assertEqual((0, 0), find_index_at_length(['aaaaaaa\taa', 'aaaaaaaaaaaaaaaaaaaaaaaa\n'], 0, 1))
        
    def test_check_nesting(self):
        print '\ntest_check_nesting'
        self.assertEqual(['<a>', '<b>', '<c>', '<d>', '<e>', '<f>', '<g>', '<h>', '<i>', '</i>', '</h>', '</g>', '</f>', '</e>', '</d>', '</c>', '</b>', '</a>'] , check_nesting(['<a>','<b>','<c>','<d>','<e>','<f>','<g>','<h>','<i>','</h>','</i>','</g>','</f>','</e>','</d>','</c>','</b>','</a>']))
        self.assertEqual(['<a>', '1', '<b>', '2', '<c>', '3', '</c>', '4', '</b>', '5', '</a>'] , check_nesting(['<a>','1','<b>','2','<c>','3','</c>','4','</b>','5','</a>']))
        self.assertEqual(['<a>', '1', '<b>', '2', '<c>', '3', '</c>', '</b>', '4', '</a>', '5'] , check_nesting(['<a>','1','<b>','2','<c>','3','</b>','4','</c>','5','</a>']))
        self.assertEqual(['<a>', '1', '<b>', '2', '<c>', '3', '<d>', '4', '</d>', '</c>', '</b>', '</a>'] , check_nesting(['<a>','1','<b>','2','<c>','3','<d>','4','</a>']))
        

unittest.main()
