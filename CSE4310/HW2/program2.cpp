#include <iostream>
#include <string>
#include "opencv2/opencv.hpp"
#define NUM_COMNMAND_LINE_ARGUMENTS 1


int main(int argc, char **argv)
{
    cv::Mat imageIn;

    // validate and parse the command line arguments
    if(argc != NUM_COMNMAND_LINE_ARGUMENTS + 1)
    {
        std::printf("USAGE: %s <image_path> \n", argv[0]);
        return 0;
    }
    else
    {
        imageIn = cv::imread(argv[1], cv::IMREAD_COLOR);

        // check for file error
        if(!imageIn.data)
        {
            std::cout << "Error while opening file " << argv[1] << std::endl;
            return 0;
        }
    }

    // Image size information
    /*std::cout << "image width: " << imageIn.size().width << std::endl;
    std::cout << "image height: " << imageIn.size().height << std::endl;
    std::cout << "image channels: " << imageIn.channels() << std::endl;*/

    // convert to grayscale
    cv::Mat imageGray;
    cv::cvtColor(imageIn, imageGray, cv::COLOR_BGR2GRAY);

    // find edges
    cv::Mat imageEdges;
    const double cannyThreshold1 = 100;
    const double cannyThreshold2 = 200;
    const int cannyAperture = 3;
    cv::Canny(imageGray, imageEdges, cannyThreshold1, cannyThreshold2, cannyAperture);
    
    // erode and dilate the edges to remove noise
    int morphologySize = 1;
    cv::Mat edgesDilated;
    cv::dilate(imageEdges, edgesDilated, cv::Mat(), cv::Point(-1, -1), morphologySize);
    cv::Mat edgesEroded;
    cv::erode(edgesDilated, edgesEroded, cv::Mat(), cv::Point(-1, -1), morphologySize);
    
    // locate the image contours (after applying a threshold or canny)
    std::vector<std::vector<cv::Point> > contours;
    //std::vector<int> hierarchy;
    cv::findContours(edgesEroded, contours, cv::RETR_EXTERNAL, cv::CHAIN_APPROX_SIMPLE, cv::Point(0, 0));

    // draw contours
    cv::Mat imageContours = cv::Mat::zeros(imageEdges.size(), CV_8UC3);
    cv::RNG rand(12345);
    for(int i = 0; i < contours.size(); i++)
    {
        cv::Scalar color = cv::Scalar(rand.uniform(0, 256), rand.uniform(0,256), rand.uniform(0,256));
        cv::drawContours(imageContours, contours, i, color);
    }

    // compute minimum area bounding rectangles
    std::vector<cv::RotatedRect> minAreaRectangles(contours.size());
    for(int i = 0; i < contours.size(); i++)
    {
        // compute a minimum area bounding rectangle for the contour
        minAreaRectangles[i] = cv::minAreaRect(contours[i]);
        
    }

    // draw the rectangles
    cv::Mat imageRectangles = cv::Mat::zeros(imageEdges.size(), CV_8UC3);
    for(int i = 0; i < contours.size(); i++)
    {
        cv::Scalar color = cv::Scalar(rand.uniform(0, 256), rand.uniform(0,256), rand.uniform(0,256));
        cv::Point2f rectanglePoints[4];
        minAreaRectangles[i].points(rectanglePoints);
        for(int j = 0; j < 4; j++)
        {
            cv::line(imageRectangles, rectanglePoints[j], rectanglePoints[(j+1) % 4], color);
        }
    }

    // fit ellipses to contours containing sufficient inliers
    std::vector<cv::RotatedRect> fittedEllipses(contours.size());
    for(int i = 0; i < contours.size(); i++)
    {
        // compute an ellipse only if the contour has more than 5 points (the minimum for ellipse fitting)
        if(contours.at(i).size() > 5)
        {
            fittedEllipses[i] = cv::fitEllipse(contours[i]);
        }
    }


    //initialize total price and amount of each coin
    float money=0;
    int quarter=0;
    int dime=0;
    int nickle=0;
    int penny=0;

    //cv::Mat imageEllipse = cv::Mat::zeros(imageEdges.size(), CV_8UC3);
    //^^ create a black canvas to draw elipses

    // draw the ellipses
    const int minEllipseInliers = 50;
    for(int i = 0; i < contours.size(); i++)
    {
        // draw ellipses with sufficient inliers(on the black canvas)
        if(contours.at(i).size() > minEllipseInliers && fittedEllipses[i].size.width > 100)
        {
            //cv::Scalar color = cv::Scalar(rand.uniform(0, 256), rand.uniform(0,256), rand.uniform(0,256));
            //cv::ellipse(imageEllipse, fittedEllipses[i], color, 2);

            //print elipse width(for debugging)
            //std::cout<<fittedEllipses[i].size.width<<std::endl;

            //if ellipse width is within the bounds, update coin count and total value
            //color of the ellipse depends on the coin type
            if(fittedEllipses[i].size.width >182 && fittedEllipses[i].size.width <189)
            {
                cv::Scalar color = cv::Scalar(0,255,0);
                cv::ellipse(imageIn, fittedEllipses[i], color, 2);
                money=money+.25;
                quarter++;
            }
            if(fittedEllipses[i].size.width >134 && fittedEllipses[i].size.width <140)
            {
                cv::Scalar color = cv::Scalar(255,0,0);
                cv::ellipse(imageIn, fittedEllipses[i], color, 2);
                money=money+.10;
                dime++;
            }
            if(fittedEllipses[i].size.width >154 && fittedEllipses[i].size.width <167)
            {
                cv::Scalar color = cv::Scalar(0,255,255);
                cv::ellipse(imageIn, fittedEllipses[i], color, 2);
                money=money+.05;
                nickle++;
            }
            if(fittedEllipses[i].size.width >143 && fittedEllipses[i].size.width <151)
            {
                cv::Scalar color = cv::Scalar(0,0,255);
                cv::ellipse(imageIn, fittedEllipses[i], color, 2);
                money=money+.01;
                penny++;
            }
        }
    }

    //print out total amount of each coin and the total price in the picture
    std::cout<<"Quarter - "<<quarter<<"\n"<<"Dime - "<<dime<<"\n"<<"Nickle - "<<nickle<<"\n"<<"Penny - "<<penny<<"\n"<<std::endl;
    std::cout<<"Total: "<<money<<std::endl;

    // display various images from the pipline
    
    /*cv::imshow("imageGray", imageGray);
    cv::imshow("imageEdges", imageEdges);
    cv::imshow("edges dilated", edgesDilated);
    cv::imshow("edges eroded", edgesEroded);
    cv::imshow("imageContours", imageContours);
    cv::imshow("imageRectangles", imageRectangles);
    cv::imshow("imageEllipse", imageEllipse);*/

    cv::imshow("imageIn", imageIn);    
    cv::waitKey();
}
