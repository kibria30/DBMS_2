import numpy as np
import cv2
from typing import Tuple, List
import matplotlib.pyplot as plt

class KMeans:
    def __init__(self, k: int, max_iters: int = 100):
        self.k = k
        self.max_iters = max_iters
        self.centroids = None
        
    def fit(self, X: np.ndarray) -> np.ndarray:
        # Randomly initialize centroids
        idx = np.random.choice(len(X), self.k, replace=False)
        self.centroids = X[idx]
        
        for _ in range(self.max_iters):
            # Assign points to nearest centroid
            distances = np.sqrt(((X - self.centroids[:, np.newaxis])**2).sum(axis=2))
            labels = np.argmin(distances, axis=0)
            
            # Update centroids
            new_centroids = np.array([X[labels == k].mean(axis=0) for k in range(self.k)])
            
            # Check convergence
            if np.all(self.centroids == new_centroids):
                break
                
            self.centroids = new_centroids
            
        return labels

def detect_skin(image_path: str, k: int = 3) -> Tuple[np.ndarray, List[np.ndarray]]:
    # Read and preprocess image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Reshape image for clustering
    pixels = img.reshape(-1, 3)
    
    # Apply K-means clustering
    kmeans = KMeans(k=k)
    labels = kmeans.fit(pixels)
    
    # Reshape labels back to image dimensions
    segmented = labels.reshape(img.shape[:2])
    
    # Create separate clusters
    clusters = []
    for i in range(k):
        cluster_mask = (segmented == i).astype(np.uint8)
        cluster = img.copy()
        cluster[cluster_mask == 0] = 0
        clusters.append(cluster)
    
    # Identify skin cluster (assuming lightest cluster is skin)
    # Calculate average brightness for each cluster
    brightness_scores = []
    for cluster in clusters:
        brightness = np.mean(cv2.cvtColor(cluster, cv2.COLOR_RGB2GRAY))
        brightness_scores.append(brightness)
    
    skin_cluster_idx = np.argmax(brightness_scores)
    skin_mask = (segmented == skin_cluster_idx).astype(np.uint8)
    
    return skin_mask, clusters

def visualize_results(img_path: str, cluster: int=3):
    # Detect skin and get clusters
    skin_mask, clusters = detect_skin(img_path, cluster)
    
    # Original image
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Apply mask to get skin regions
    skin_detected = img.copy()
    skin_detected[skin_mask == 0] = 0
    
    # Visualize results
    plt.figure(figsize=(15, 5))
    
    plt.subplot(121)
    plt.imshow(img)
    plt.title('Original Image')
    plt.axis('off')
    
    # plt.subplot(132)
    # plt.imshow(skin_mask, cmap='gray')
    # plt.title('Skin Mask')
    # plt.axis('off')
    
    plt.subplot(122)
    plt.imshow(skin_detected)
    plt.title('Detected Skin')
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

visualize_results('/home/kibria/Desktop/DBMS/DBMS_2/kmeans/hand.jpg', 2)