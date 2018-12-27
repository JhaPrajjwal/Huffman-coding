import heapq

class node:
    def __init__(self,char,freq):
        self.char = char
        self.frequency = freq
        self.left = None
        self.right = None

    def __gt__(self, other):
        if other == None:
            return -1

        return self.frequency > other.frequency

class huffmancoding:
    def __init__(self):
        self.minheap = []
        self.codes = {}
        self.compressed = ""
        self.root = None
        self.reverse_codes = {}

    def get_frequency(self,data):
        freq = {}
        for i in data:
            if i not in freq:
                freq[i] = 1
            else:
                freq[i] += 1

        return freq

    def make_heap(self,frequency):
        for k in frequency:
            temp = node(k,frequency[k])
            heapq.heappush(self.minheap,temp)

        while len(self.minheap)>1:
            left = heapq.heappop(self.minheap)
            right = heapq.heappop(self.minheap)

            temp = node(None,left.frequency+right.frequency)
            temp.left = left
            temp.right = right

            heapq.heappush(self.minheap,temp)

        self.root = heapq.heappop(self.minheap)


    def build_codes(self,root,code):
        if root == None:
            return

        if root.char != None:
            self.codes[root.char] = code
            self.reverse_codes[code] = root.char
            return

        self.build_codes(root.left, code + "0")
        self.build_codes(root.right, code + "1")


    def compress(self,file):

        f = open(file,'r')
        data = f.read()
        f.close()

        freq = self.get_frequency(data)
        self.make_heap(freq)
        self.build_codes(self.root,"")

        for i in data:
            self.compressed += self.codes[i]

        """
            As data is stored as bytes convert them to multiple of 8 (1 byte = 8 bits).
        """
        left = 8-len(self.compressed)%8
        add = '0'*left


        """
            Add information about how many bytes were added.
        """
        add = "{0:08b}".format(left)+add
        self.compressed = add + self.compressed

        b = bytearray()
        for i in range(0,len(self.compressed),8):
            byte = self.compressed[i:i+8]
            b.append(int(byte, 2))

        f = open("compressed.bin",'wb')
        f.write(bytes(b))
        f.close()
        return "compressed.bin"



    def decompress(self,file):
        f = open(file,'rb')
        data = f.read()
        f.close()

        encoded = ""
        for byte in data:
            encoded += bin(byte)[2:].rjust(8,'0')

        encoded = encoded[8+data[0]:] #removing the extra info
        code = ""
        output = ""
        for i in encoded:
            code += i
            if code in self.reverse_codes.keys():
                output += self.reverse_codes[code]
                code = ""

        f = open("output.txt",'w')
        f.write(output)
        f.close()


def main():
    obj = huffmancoding()
    Compressed_filename = obj.compress("input.txt")
    obj.decompress(Compressed_filename)
