#include <stdio.h>
#include <iostream>
#include "opencv2/opencv.hpp"
#include "opencv2/imgproc/imgproc_c.h"
#include <stdio.h>
#include <iostream>
#include "opencv2/opencv.hpp"
#include "opencv2/imgproc/imgproc_c.h"
// configuration parameters
#define NUM_COMNMAND_LINE_ARGUMENTS 5

int main(int argc, char **argv)
{
    // store video capture parameters
    std::string fileName;
    cv::Mat captureFrame;
    cv::Mat captureFrameGray;
    cv::Mat imageTemplate1;
    cv::Mat imageTemplate2;
    cv::Mat imageTemplate3;
    cv::Mat imageTemplate4;
    cv::Mat imageTemplateGray;
    cv::Mat searchResult1;
    cv::Mat searchResult2;
    cv::Mat searchResult3;
    cv::Mat searchResult4;
    std::vector<cv::Point> matchesTemplateVec;
    

    if(argc != NUM_COMNMAND_LINE_ARGUMENTS + 1)
    {
        std::printf("USAGE: %s <../file_path> <../template_image>\n", argv[0]);
        return 0;
    }
    else
    {
        fileName = argv[1];
        imageTemplate1 = cv::imread(argv[2], cv::IMREAD_COLOR);
        imageTemplate2 = cv::imread(argv[3], cv::IMREAD_COLOR);
        imageTemplate3 = cv::imread(argv[4], cv::IMREAD_COLOR);
        imageTemplate4 = cv::imread(argv[5], cv::IMREAD_COLOR);
    }

    // open the video file
    cv::VideoCapture capture(fileName);
    if(!capture.isOpened())
    {
        std::printf("Unable to open video source, terminating program! \n");
        return 0;
    }

    int captureWidth = static_cast<int>(capture.get(cv::CAP_PROP_FRAME_WIDTH));//1200
    int captureHeight = static_cast<int>(capture.get(cv::CAP_PROP_FRAME_HEIGHT));//1000
    //std::cout << "Video source opened successfully (width=" << captureWidth << " height=" << captureHeight << ")!" << std::endl;


    // process data until program termination
    bool doCapture = true;
    int frameCount = 0;
    while(doCapture)
    {
        // attempt to acquire and process an image frame
        bool captureSuccess = capture.read(captureFrame);
        if(captureSuccess)
        {
            //cv::cvtColor(imageTemplate, imageTemplateGray, cv::COLOR_BGR2GRAY);
            //cv::cvtColor(captureFrame, captureFrameGray, cv::COLOR_BGR2GRAY);

            // perform the matching step and normalize the searchResult
            int match_method = cv::TM_CCORR_NORMED;
            cv::matchTemplate(captureFrame, imageTemplate1, searchResult1, match_method);
            cv::matchTemplate(captureFrame, imageTemplate2, searchResult2, match_method);
            cv::matchTemplate(captureFrame, imageTemplate3, searchResult3, match_method);
            cv::matchTemplate(captureFrame, imageTemplate4, searchResult4, match_method);

            cv::normalize(searchResult1, searchResult1, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());
            cv::normalize(searchResult2, searchResult2, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());
            cv::normalize(searchResult3, searchResult3, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());
            cv::normalize(searchResult4, searchResult4, 0, 1, cv::NORM_MINMAX, -1, cv::Mat());

            double maxVal1, minVal1,maxVal2, minVal2,maxVal3, minVal3,maxVal4, minVal4;
            cv::Point maxLocation1, minLocation1,maxLocation2, minLocation2,maxLocation3, minLocation3,maxLocation4, minLocation4;
            double threshold = .9;

            cv::minMaxLoc(searchResult1, &minVal1, &maxVal1, &minLocation1, &maxLocation1, cv::Mat());
            cv::minMaxLoc(searchResult2, &minVal2, &maxVal2, &minLocation2, &maxLocation2, cv::Mat());
            cv::minMaxLoc(searchResult3, &minVal3, &maxVal3, &minLocation3, &maxLocation3, cv::Mat());
            cv::minMaxLoc(searchResult4, &minVal4, &maxVal4, &minLocation4, &maxLocation4, cv::Mat());

            //set color of the bounding boxes  20 30

            cv::Vec3b color1 = imageTemplate1.at<cv::Vec3b>(cv::Point(20,30));
            cv::Vec3b color2 = imageTemplate2.at<cv::Vec3b>(cv::Point(20,30));
            cv::Vec3b color3 = imageTemplate3.at<cv::Vec3b>(cv::Point(20,30));
            cv::Vec3b color4 = imageTemplate4.at<cv::Vec3b>(cv::Point(20,30));
            /*std::cout<<imageTemplate1.rows<<","<<imageTemplate1.cols<<std::endl;
             std::cout<<imageTemplate2.rows<<","<<imageTemplate2.cols<<std::endl;
              std::cout<<imageTemplate3.rows<<","<<imageTemplate3.cols<<std::endl;
               std::cout<<imageTemplate4.rows<<","<<imageTemplate4.cols<<std::endl;*/
           


            if(maxVal1>threshold)
            {
                
                cv::rectangle(captureFrame, maxLocation1, cv::Point(maxLocation1.x + imageTemplate1.cols , maxLocation1.y + imageTemplate1.rows), color1, 5);

            }
            if(maxVal2>threshold)
            {
                
                cv::rectangle(captureFrame, maxLocation2, cv::Point(maxLocation2.x + imageTemplate2.cols , maxLocation2.y + imageTemplate2.rows), color2, 5);

            }
            if(maxVal3>threshold)
            {
                
                cv::rectangle(captureFrame, maxLocation3, cv::Point(maxLocation3.x + imageTemplate3.cols , maxLocation3.y + imageTemplate3.rows), color3, 5);

            }
            if(maxVal4>threshold)
            {
                
                cv::rectangle(captureFrame, maxLocation4, cv::Point(maxLocation4.x + imageTemplate4.cols , maxLocation4.y + imageTemplate4.rows), color4, 5);

            }
            
            //iterate through every pixel and find oe=nes over the threshold
            /*for(int x=0 ; x<searchResult.cols; ++x)//cols-1
            {
                std::cout<<"Test x:  "<<x<<std::endl;
                for(int y = 0; y<searchResult.rows ; ++y)//rows-1
                {
                    std::cout<<"Test Y:  "<<y<<std::endl;
                    if(searchResult.at<double>(cv::Point(x,y))>threshold)
                    {
                        //std::cout<<"HOAL"<<std::endl;
                        cv::rectangle(captureFrame, cv::Point(x,y), cv::Point(maxLocation1.x + imageTemplate.cols , maxLocation1.y + imageTemplate.rows), CV_RGB(255,0,255), 5);
                    }      
                }
            }*/
            //cv::rectangle(captureFrame, maxLocation1, cv::Point(maxLocation1.x + imageTemplate.cols , maxLocation1.y + imageTemplate.rows), CV_RGB(255,0,255), 5);
            //std::cout<<"searchResult[x]: "<< searchResult[0]<<std::endl;
           
            // increment the frame counter
            frameCount++;
        }
        else
        {
            std::printf("Unable to acquire image frame! \n");
        }

        // update the GUI window if necessary
        if(captureSuccess)
        {
            //cv::imshow("searchResult", searchResult);
            cv::imshow("Capture Frame", captureFrame);
            //cv::imshow("imageTemplate", imageTemplate);
            // check for program termination
            if(((char) cv::waitKey(1)) == 'q')
            {
                doCapture = false;
            }
        }
    }

    // release program resources before returning
    capture.release();
    cv::destroyAllWindows();
}