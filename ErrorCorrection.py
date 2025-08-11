import numpy as np

def create_matrix(m, n):
    # Create an m x n matrix filled with zeros
    return np.zeros((m, n), dtype=int)

def generate_parity_matrix(matrix):
    # Generate a parity-check matrix by adding parity bits to each column
    m, n = matrix.shape
    parity_matrix = create_matrix(m, n+1)
    parity_matrix[:,:n] = matrix
    for i in range(n):
        parity_matrix[:,n] ^= parity_matrix[:,i]
    return parity_matrix

def generate_generator_matrix(m, r):
    # Generate a generator matrix using the standard construction for Hamming codes
    n = 2**r - 1
    k = n - r
    g_matrix = create_matrix(k, n)
    for i in range(k):
        for j in range(n):
            if ((j+1) & (1 << i)) != 0:
                g_matrix[i,j] = 1
    return g_matrix

def encode_message(message, g_matrix):
    # Encode a message using the generator matrix
    codeword = np.dot(message, g_matrix) % 2
    return codeword

def decode_message(received_message, parity_matrix):
    # Decode a received message using the parity-check matrix
    m, n = parity_matrix.shape
    syndrome = np.dot(parity_matrix, received_message) % 2
    error_index = 0
    for i in range(n):
        if np.array_equal(syndrome, parity_matrix[:,i]):
            error_index = i+1
            break
    if error_index != 0:
        received_message[error_index-1] = (received_message[error_index-1]+1) % 2
    return received_message

# Example usage:
message = np.array([1,0,1,1])
r = 3 # Number of parity bits
g_matrix = generate_generator_matrix(len(message), r)
parity_matrix = generate_parity_matrix(g_matrix)
codeword = encode_message(message, g_matrix)
print("Original message:", message)
print("Codeword:", codeword)
received_message = np.array([1,0,0,1,1,0,1])
decoded_message = decode_message(received_message, parity_matrix)
print("Received message:", received_message)
print("Decoded message:", decoded_message)
