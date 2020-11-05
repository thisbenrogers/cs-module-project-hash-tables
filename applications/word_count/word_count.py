def word_count(s):
    # * sets up dictionary
    table = {}

    # * base check
    if len(s) <= 0:
        return table

    # * clears irrelevant characters and converts s to lowercase
    ignore = '":;,.-+=/\|[]{}()*^&'
    new_s = s.lower()

    for char in ignore:
        new_s = new_s.replace(char, "")

    # * creates a list using each word in the string
    s_arr = new_s.split()

    # * iterates through list, tallying a count for each entry
    for word in s_arr:
        if word in table:
            table[word] += 1
        else:
            table[word] = 1
    
    return table



if __name__ == "__main__":
    print(word_count(""))
    print(word_count("Hello"))
    print(word_count('Hello, my cat. And my cat doesn\'t say "hello" back.'))
    print(word_count('This is a test of the emergency broadcast network. This is only a test.'))