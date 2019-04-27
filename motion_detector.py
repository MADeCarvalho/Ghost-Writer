import numpy as np
import cv2

# def getSector(base, width, height, num_sectors):
#     sectors = []
#     for i in range(1, num_sectors+1):
#         sectors.append(base[,])

def captureBase(cap, num_sectors):
    s, base = cap.read()
    b_width, b_height , b_layers = base.shape
    b_sector_width = round(b_width/num_sectors/2)
    b_sector_height = round(b_height/num_sectors/2)

    b_sector_1 = base[:b_sector_width, :b_sector_height,:]
    b_sector_2 = base[b_sector_width:, :b_sector_height,:]
    b_sector_3 = base[:b_sector_width, b_sector_height:,:]
    b_sector_4 = base[b_sector_width:, b_sector_height:,:]

    b_sector_1_ave = np.mean(b_sector_1[:,:])
    b_sector_2_ave = np.mean(b_sector_2[:,:])
    b_sector_3_ave = np.mean(b_sector_3[:,:])
    b_sector_4_ave = np.mean(b_sector_4[:,:])

    sector_1_std = np.std(b_sector_1[:,:])
    sector_2_std = np.std(b_sector_2[:,:])
    sector_3_std = np.std(b_sector_3[:,:])
    sector_4_std = np.std(b_sector_4[:,:])

    return((b_sector_1_ave, b_sector_2_ave, b_sector_3_ave, b_sector_4_ave, sector_1_std, sector_2_std, sector_3_std, sector_4_std ))

if __name__ == "__main__":

    cap = cv2.VideoCapture(0)  # 0 -> index of camera    
    i = 100
    num_sectors = 4

    while(True):

        if ((i % 100) == 0):
            b_sector_1_ave, b_sector_2_ave, b_sector_3_ave, b_sector_4_ave, sector_1_std, sector_2_std, sector_3_std, sector_4_std  = captureBase(cap, num_sectors)

        i = i + 1

        # Capture frame-by-frame
        ret, frame = cap.read()
        motion_detected = False
        motion_detected_1 = False
        motion_detected_2 = False
        motion_detected_3 = False
        motion_detected_4 = False

        # Our operations on the frame come here
        width, height , layers = frame.shape
        sector_width = round(width/2)
        sector_height = round(height/2)

        sector_1 = frame[:sector_width, :sector_height,:]
        sector_2 = frame[sector_width:, :sector_height,:]
        sector_3 = frame[:sector_width, sector_height:,:]
        sector_4 = frame[sector_width:, sector_height:,:]

        sector_1_ave = np.mean(sector_1[:,:])
        sector_2_ave = np.mean(sector_2[:,:])
        sector_3_ave = np.mean(sector_3[:,:])
        sector_4_ave = np.mean(sector_4[:,:])

        print((b_sector_1_ave, b_sector_2_ave, b_sector_3_ave, b_sector_4_ave))
        print((sector_1_ave, sector_2_ave, sector_3_ave, sector_4_ave))

        print((sector_1_std, sector_2_std, sector_3_std, sector_4_std))

        print((abs(sector_1_ave - b_sector_1_ave), abs(sector_2_ave - b_sector_2_ave), abs(sector_3_ave - b_sector_3_ave), abs(sector_4_ave - b_sector_4_ave)))
        print((abs(sector_1_ave - b_sector_1_ave) > sector_1_std), (abs(sector_2_ave - b_sector_2_ave) > sector_2_std), (abs(sector_3_ave - b_sector_3_ave) > sector_3_std), (abs(sector_4_ave - b_sector_4_ave) > sector_4_std))

        motion_detected_1 = True if (abs(sector_1_ave - b_sector_1_ave)  > 2*sector_1_std) else False
        motion_detected_2 = True if (abs(sector_2_ave - b_sector_2_ave)  > 2*sector_2_std) else False
        motion_detected_3 = True if (abs(sector_3_ave - b_sector_3_ave)  > 2*sector_3_std) else False
        motion_detected_4 = True if (abs(sector_4_ave - b_sector_4_ave)  > 2*sector_4_std) else False

        if (motion_detected_1 or motion_detected_2 or motion_detected_3 or motion_detected_4):
            motion_detected = True
            sector_1[:, :] = sector_1[:, :] if (not motion_detected_1) else (0, 0, 255)
            sector_2[:, :] = sector_2[:, :] if (not motion_detected_2) else (0, 0, 255)
            sector_3[:, :] = sector_3[:, :] if (not motion_detected_3) else (0, 0, 255)
            sector_4[:, :] = sector_4[:, :] if (not motion_detected_4) else (0, 0, 255)

            print("motion detected!")
        #else:
           # print("no motion detected!")

        # Display the resulting frame
        cv2.imshow('sector 1', sector_1)
        cv2.imshow('sector 2', sector_2)
        cv2.imshow('sector 3', sector_3)
        cv2.imshow('sector 4', sector_4)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()