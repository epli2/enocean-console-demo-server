# -*- coding: utf-8 -*-
import math

# https://gist.github.com/adammiller/826148/1d85ef082868391b3e0d13865dfc098705d1c30d
def simplifyPath(origpoints, tolerance):
    if tolerance <= 0:
        return origpoints
    points = [{'x': i, 'y': v['value'], 'ret': v['ret'], 'timestamp': v['timestamp'], 'topic': v['topic']} for i, v in enumerate(origpoints)]

    class Line:
        def __init__(self, p1, p2):
            self.p1 = p1
            self.p2 = p2

        def distanceToPoint(self, point):
            # slope
            m = (self.p2['y'] - self.p1['y']) / (self.p2['x'] - self.p1['x'])
            # y offset
            b = self.p1['y'] - (m * self.p1['x'])
            d = []
            # distance to the linear equation
            d.append(abs(point['y'] - (m * point['x']) - b) / math.sqrt(pow(m, 2) + 1))
            # distance to p1
            d.append(math.sqrt(
                pow((point['x'] - self.p1['x']), 2) +
                pow((point['y'] - self.p1['y']), 2)))
            # distance to p2
            d.append(math.sqrt(
                pow((point['x'] - self.p2['x']), 2) +
                pow((point['y'] - self.p2['y']), 2)))
            # return the smallest distance
            return min(d)
            # causes an array to be sorted numerically and ascending

    def douglasPeucker(points, tolerance):
        returnPoints = []
        if (len(points) <= 2):
            return [points[0]]
        # make line from start to end
        line = Line(points[0], points[len(points) - 1])
        # find the largest distance from intermediate poitns to this line
        maxDistance = 0
        maxDistanceIndex = 0
        for i in range(1, len(points) - 2):
            distance = line.distanceToPoint(points[i])
            if (distance > maxDistance):
                maxDistance = distance
                maxDistanceIndex = i
        # check if the max distance is greater than our tollerance allows
        if (maxDistance >= tolerance):
            p = points[maxDistanceIndex]
            line.distanceToPoint(p)
            # include this point in the output
            returnPoints += douglasPeucker(points[0:maxDistanceIndex + 1], tolerance)
            # returnPoints.append( points[maxDistanceIndex] )
            returnPoints += douglasPeucker(points[maxDistanceIndex:len(points)], tolerance)
        else:
            # ditching this point
            p = points[maxDistanceIndex]
            line.distanceToPoint(p)
            returnPoints = [points[0]]
        return returnPoints
    arr = douglasPeucker(points, tolerance)
    # always have to push the very last point on so it doesn't get left off
    arr.append(points[len(points) - 1])
    return [{'value': v['y'], 'ret': v['ret'], 'timestamp': v['timestamp'], 'topic': v['topic']} for i, v in enumerate(arr)]
