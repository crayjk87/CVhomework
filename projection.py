import numpy as np

def get_points(filename):
    points = []
    with open(filename,'r') as f:
        for data in f.readlines():
            data = data.split()
            data = [float(i) for i in data]
            points.append(data)
        points_data = np.array(points)

    return points_data

# AP = 0, Xt(AtA)X>=0, 
def get_proj(p2d, p3d):
    A = np.zeros((2 * np.size(p3d,0), 12))

    for i, num in enumerate(zip(p3d,p2d)):
        point_3d = np.append(num[0],[1])
        point_2d_x = np.array([-num[1][0]*num[0][0], -num[1][0]*num[0][1], -num[1][0]*num[0][2], -num[1][0]])
        point_2d_y = np.array([-num[1][1]*num[0][0], -num[1][1]*num[0][1], -num[1][1]*num[0][2], -num[1][1]])

        A[i*2][0:4] = point_3d
        A[i*2][8:] = point_2d_x
        A[i*2 + 1][4:8] = point_3d
        A[i*2 + 1][8:] = point_2d_y

    #print(np.matmul(A.T, A).shape)
    eigen_val, eigen_vec = np.linalg.eig(np.matmul(A.T,A))
    proj_mat = eigen_vec[:, np.argmin(eigen_val)].reshape(3,4)
    

    return proj_mat


def get_rotate(mat):
    M = mat[:,0:3]
    M_inv = np.linalg.inv(M)
    Q, _ = np.linalg.qr(M_inv)
    return np.linalg.inv(Q)


def get_calib(mat):
    M = mat[:,0:3]
    M_inv = np.linalg.inv(M)
    _, R = np.linalg.qr(M_inv)
    return np.linalg.inv(R)
    

def get_trans(mat, K):
    P_4 = mat[:,3:]
    return np.matmul(np.linalg.inv(K), P_4)


def cal_average_err(mat, p3d, p2d):
    p3d = np.c_[p3d, np.ones(np.size(p3d,0))].T
    PX = np.matmul(mat, p3d)
    #PX = np.delete(PX, np.size(PX,0)-1, axis=0)
    #print(np.shape(PX))
    new_x = PX[0] / PX[2]
    new_y = PX[1] / PX[2]
    #print(np.shape(new_x))
    #print(np.shape(PX))
    new_PX = np.array([new_x, new_y])
    #print(np.shape(new_PX))
    err = np.sqrt((np.power(p2d.T - new_PX, 2)).sum(axis=0)).sum()
    avg_err = err / np.size(PX,1)
    #print(avg_err)
    
    return avg_err


def main():
    point_2d = get_points('points2D.txt')
    point_3d = get_points('points3D.txt')
    
    projection_matrix = get_proj(point_2d, point_3d)
    print('The projection matrix is:')
    print(projection_matrix)
    np.savetxt("P.csv", projection_matrix, delimiter=",")

    rotation_matrix = get_rotate(projection_matrix)
    print('The rotation matrix is:')
    print(rotation_matrix)
    np.savetxt("R.csv", rotation_matrix, delimiter=",")

    calibration_matrix = get_calib(projection_matrix)
    print('The calibration matrix is:')
    print(calibration_matrix)
    np.savetxt("K.csv", calibration_matrix, delimiter=",")

    translation_matrix = get_trans(projection_matrix, calibration_matrix)
    print('The translation matrix is:')
    print(translation_matrix)
    np.savetxt("T.csv", translation_matrix, delimiter=",")


    err = cal_average_err(projection_matrix, point_3d, point_2d)
    print('The average projection error is:')
    print(err)



     

if __name__ == '__main__':
    main()
        