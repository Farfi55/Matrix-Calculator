# def read_matrix():
#     n, m = [int(x) for x in input().split()]     
#     return [[int(x) for x in input().split()] for y in range(n)]   
     
# def add_matrices(A, B):
#     if (len(A) == 0 or len(A) != len(B) or len(A[0]) != len(B[0])):
#         print("ERROR")
#         return None
        
#     return [[A[i][j] + B[i][j] for j in range(len(A[0]))] for i in range(len(A))]  
    
JET_BRAINS_MODE = True

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def print_menu():
    print("""
1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit""")

def print_transpose_options():
    print("""
1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line""")



def read_command(start=0, end=6):
    print("Your choise: ", end="" if JET_BRAINS_MODE else "> ")
    choise = input()

    if choise.isdigit():
        choise = int(choise)
        if start <= choise <= end:
            return choise
    
    return -1

def read_matrix_size(matrix_name=""):
    print(f"Enter size of {matrix_name}matrix: ", end="" if JET_BRAINS_MODE else "> ")
    dirty_input = input().split()
    if len(dirty_input) == 2:
        n, m = dirty_input
        if n.isdigit() and m.isdigit():
            return int(n), int(m)
    
    return -1, -1

def read_matrix_size_safe(matrix_name=""):
    while True:
        n,m = read_matrix_size(matrix_name)
        if n > 0 and m > 0:
            return n, m

        print("Error, size not valid")

def read_square_matrix_size_safe(matrix_name=""):
    while True:
        n,m = read_matrix_size(matrix_name)
        if n > 0 and n == m:
            return n, m

        print("Error, size not valid, rows and columns must be the same")
    


def read_matrix(rows,columns, rows_info=True, custom_prompt=""):
    matrix = []

    print(f"enter {custom_prompt}matrix:")
    for i in range(rows):
        while True:
            all_correct = True
            row = []    
            if not JET_BRAINS_MODE:
                print(f"row {i+1}: ",end="")
            dirty_elements = list(input().split())

            if len(dirty_elements) != columns:
                if JET_BRAINS_MODE: print("The operation cannot be performed.")
                else: print(f"Error, you should enter {columns} elements instead of {len(dirty_elements)}")
                continue
            for dirty_element in dirty_elements:
                if not isfloat(dirty_element):
                    print("Error, re-enter row!")
                    all_correct = False
                    break
                row.append(float(dirty_element))
            if all_correct:
                matrix.append(row)
                break
            
    return matrix
            
def get_matrix_size(matrix):
    return len(matrix), len(matrix[0])
    
def print_matrix(matrix, rows_info=True, custom_type=None):
    rows, columns = get_matrix_size(matrix)
    for i in range(rows):
        if (not JET_BRAINS_MODE) and rows_info:
            print(f"row {i+1}: ", end="")
        
        for j in range(columns):
            element = matrix[i][j]
            if custom_type is not None:
                if JET_BRAINS_MODE: print(f"{custom_type(element)}", end=" ")
                else: print(f"{custom_type(element):6}", end=" ")
            else: 
                if JET_BRAINS_MODE: print(f"{element}", end=" ")
                else: print(f"{element:6}", end=" ")
                
        print()
        



def is_same_size_matrices(a_matrix, b_matrix, *extra_matrices):
    if get_matrix_size(a_matrix) !=  get_matrix_size(b_matrix):
        return False

    for extra_matrice in extra_matrices:
        if get_matrix_size(a_matrix) != get_matrix_size(extra_matrice):
            return False

    return True


def add_matrices(a_matrix, b_matrix, *extra_matrices):
    if not is_same_size_matrices(a_matrix, b_matrix, *extra_matrices):
        print("Error, size does not match!")
        return None

    rows, columns = get_matrix_size(a_matrix)

    sum_matrix = a_matrix[:]
    
    for i in range(rows):
        for j in range(columns):
            sum_matrix[i][j] += b_matrix[i][j]
            for extra_matrice in extra_matrices:
                sum_matrix[i][j] += extra_matrice[i][j]
    
    return sum_matrix
    
    


def scale_matrix(scalar, matrix):
    return [[scalar * element for element in row] for row in matrix]




def multiply_matrices(a_matrix, b_matrix):
    a_rows, a_columns = get_matrix_size(a_matrix)
    b_rows, b_columns = get_matrix_size(b_matrix)
    if a_columns != b_rows:
        if not JET_BRAINS_MODE:
            print(f"Error, matrices size doesn't match, {a_rows}x{a_columns}, {b_rows}x{b_columns}")
        return None


    product_matrix = []
    for i in range(a_rows):
        product_matrix.append([])
        for j in range(b_columns):

            dot_product = sum([a_matrix[i][k] * b_matrix[k][j] for k in range(a_columns) ])

            product_matrix[i].append(dot_product)

    return product_matrix


def transpose_matrix(matrix, transpose_type=1):
    rows, cols = get_matrix_size(matrix)

    if transpose_type == 4: return matrix[::-1]
    elif transpose_type == 3: return [matrix[i][::-1] for i in range(rows)]

    transposed_matrix = [[0 for j in range(rows)] for i in range(cols)] 
        
    for i in range(rows):              
        for j in range(cols):            
            if transpose_type == 1: transposed_matrix[j][i] = matrix[i][j]
            elif transpose_type == 2: transposed_matrix[-j-1][-i-1] = matrix[i][j]

    return transposed_matrix



def minor(matrix, i, j):
    rows, cols = get_matrix_size(matrix)
    minor = [[matrix[row][col] for col in range(cols) if col != j] for row in range(rows) if row != i]
    return minor


def cofactor(matrix, i, j):
    if (i+j)%2: return -matrix[i][j]
    else:       return  matrix[i][j]


def det(matrix):
    rows, cols = get_matrix_size(matrix)

    if rows == 0 or rows != cols:
        return None
    
    if rows == 1:
        return matrix[0][0]
    elif rows == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        # can be optimized much more
        return sum( cofactor(matrix,0,j) * det(minor(matrix, 0,j)) for j in range(cols))




def main():
    command = None
    while True:
        print_menu()
        command = read_command()
        if command == -1:
            print("Error, unreconized command!")
            continue
        elif command == 0:  # Exit
            print("goodbye!")
            break
        elif command == 1:  # Add matrices            
            a_rows, a_columns = read_matrix_size_safe("first ")
            a_matrix = read_matrix(a_rows,a_columns)


            b_rows, b_columns = read_matrix_size_safe("second ")
            b_matrix = read_matrix(b_rows,b_columns)

            sum_matrix = add_matrices(a_matrix, b_matrix)
            if sum_matrix is not None:
                print("The result is:")                
                print_matrix(sum_matrix)

        
        elif command == 2: # Multiply matrix by a constant
            rows, columns = read_matrix_size_safe()
            
            matrix = read_matrix(rows, columns) 
            scalar = input("Enter constant: ")
            if not isfloat(scalar):
                print("Error, unreconized value")
                continue

            scalar = float(scalar)         
            scaled_matrix = scale_matrix(scalar,matrix)

            if scaled_matrix is not None:
                print("The result is:")              
                print_matrix(scaled_matrix)

        elif command == 3:  # Multiply matrices
            a_rows, a_columns = read_matrix_size_safe("first ")
            a_matrix = read_matrix(a_rows,a_columns)

            b_rows, b_columns = read_matrix_size_safe("second ")
            b_matrix = read_matrix(b_rows,b_columns)

            if a_columns != b_rows:
                print("The operation cannot be performed.")
                continue

            product_matrix = multiply_matrices(a_matrix,b_matrix)

            if product_matrix is not None:
                print("The result is:")              
                print_matrix(product_matrix)

        elif command == 4:  # Transpose matrix
            print_transpose_options()
            while True:
                transpose_type = read_command(1,4)
                if transpose_type == -1: print("Error, invalid type")
                else: break 
                
            rows, columns = read_matrix_size_safe()            
            matrix = read_matrix(rows, columns) 

            transposed_matrix = transpose_matrix(matrix, transpose_type)

            if transposed_matrix is not None:
                print("The result is:")              
                print_matrix(transposed_matrix)

        elif command == 5:
            rows, columns = read_square_matrix_size_safe()            
            matrix = read_matrix(rows, columns) 

            determinant = det(matrix)
            if determinant is not None:
                print("The result is:")              
                print(determinant)
        
        elif command == 6:
            rows, columns = read_square_matrix_size_safe()            


            matrix = read_matrix(rows, columns) 
            
            determinant = det(matrix)
            if determinant == 0:
                print("This matrix doesn't have an inverse.")
                continue

            cofactor_matrix = [[ det(minor(matrix, i, j)) * (-1 if (i+j)%2 else 1) for j in range(columns) ] for i in range(rows)]

            transposed_matrix = transpose_matrix(cofactor_matrix)
            inverse_matrix = scale_matrix(1 / determinant, transposed_matrix) 
            
            print("The result is:")              
            print_matrix(inverse_matrix)


        else:
            raise ValueError



if __name__ == "__main__":
    main()




