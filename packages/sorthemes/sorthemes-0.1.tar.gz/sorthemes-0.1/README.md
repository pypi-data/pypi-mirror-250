# SORTHEMES PYTHON LIBRARY BY CHRISTIAN
A simple python library for sorting and modifying lists.

# PURPOSE
Sorthemes provides simple function in order to sort and modify lists in python either you need to sort list in ascending or descending,capitalize or convert string items to upper and lowercase. this library offers straightforward methods to enhance your lists manipulation capabilities.

# SYNTAX AND USAGE
1. sort_asc() - to sort list in ascending order.
2. sort_desc() - to sort list in descending order.
3. sort_caps() - to capitalize sorted list items.
4. sort_lows() - to set items into lowercase.
5. sort_ups() - to set items into uppercase.

3 to 5 only applicable in string.

make sure you import the library
— from sorthemes import sorthemes

# Example list
my_num = [8, 2, 9, 5, 4, 1, 6, 3, 0, 7]
my_letter = ['h', 'b', 'i', 'e', 'd', 'a', 'f']

# Sort ascending
sorted_num = sorthemes.sort_asc(my_num)
sorted_letter = sorthemes.sort_asc(my_letter)
print(f"sorted num: {sorted_num}") 
print(f"sorted letter: {sorted_letter}")

# Sort descending
sorted_num = sorthemes.sort_desc(my_num)
sorted_letter = sorthemes.sort_desc(my_letter)
print(f"sorted num: {sorted_num}") 
print(f"sorted letter: {sorted_letter}")

# Capitalize sorted items
caps_letter = sorthemes.sort_caps(my_letter)
print(f"capitalize letter: {caps_letter}")

# Lowercase sorted items 
lows_letter = sorthemes.sort_lows(my_letter)
print(f"lowercase letter: {lows_letter}")

# Uppercase sorted items 
ups_letter = sorthemes.sort_ups(my_letter)
print(f"uppercase letter: {ups_letter}")

# INSTALLATION
You can install the library using pip.

— pip install sorthemes

# MIT License

Copyright (c) 2024 christian garcia

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.