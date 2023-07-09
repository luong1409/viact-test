def calculate_iou(box1, box2):
    """Calculate IOU between box1 and box2

    Args:
        box1 (coordinate): the co-ordinate of box1 
        box2 (coordinate): the co-ordinate of box2
    """
    pass

def is_parent_child(parent, child, hier):
    """Return True if "child" var is children of "parent" variable

    Args:
        parent (str): name of parent class
        child (str): name of child class
        hier (pd.DataFrame): mapper between parent and child class.
    """
    pass


def modified_nms(boxes, scores, classes, class_hierarchy, score_threshold, iou_threshold):
    """This is the modified version of Non-max suppresion algorithm.<br>
    Which is used for remove redundant bounding boxes.

    Args:
        boxes (numpy.array[coordinate]): list of coordinates of bouding box
        scores (numpy.array[float]): list of confidence scores.
        classes (numpy.array[str]): list of classes.
        class_hierarchy (pd.DataFrame): mapper for parent, child relation.
        score_threshold (float): score threshold for filtering out bounding boxes which have confident score > score_threshold.
        iou_threshold (float): IOU threshold for filtering out bouding boxes which have IOU score > iou_threshold.
    """
    
    # Step 1: Select boxes with confidence score exceeding the threshold
    selected_indices = scores >= score_threshold
    boxes = boxes[selected_indices]
    scores = scores[selected_indices]
    classes = classes[selected_indices]

    # Step 2: Sort boxes based on confidence in descending order
    sorted_indices = scores.argsort()[::-1]  # inverse the indexes
    boxes = boxes[sorted_indices]
    scores = scores[sorted_indices]
    classes = classes[sorted_indices]

    # Step 3: Apply NMS to eliminate overlapping boxes
    selected_indices = []
    for i in range(len(boxes)):
        if i not in selected_indices:
            selected_indices.append(i)

            for j in range(i + 1, len(boxes)):
                if j not in selected_indices:
                    selected_indices.append(j)
                    iou = calculate_iou(boxes[i], boxes[j])

                    # Check for highly overlapped boxes 
                    # -> IOU score is greater than iou_threshold
                    if iou > iou_threshold:
                        # If highly overlapped boxes belong to same class 
                        # -> Eliminate the box with lower confidence
                        if classes[i] == classes[j]:
                            if scores[j] > scores[i]:
                                selected_indices.remove(i)
                            elif scores[j] < scores[i]:
                                selected_indices.remove(j)

                        # If highly overlapped boxes belong to different classes 
                        # -> Eliminate the box if it's the parent class of another box
                        else:
                            class_i = classes[i]
                            class_j = classes[j]
                            if is_parent_child(class_j, class_i, class_hierarchy):
                                # remove class_j because class_j is parent of class_i
                                selected_indices.remove(j)
                            elif is_parent_child(class_i, class_j, class_hierarchy):
                                # remove class_i because class_ji is parent of class_j
                                selected_indices.remove(i)

    
    selected_boxes = boxes[selected_indices]
    selected_scores = scores[selected_indices]
    selected_classes = classes[selected_indices]

    return selected_boxes, selected_scores, selected_classes
