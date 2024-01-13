import torch
import torch.nn as nn
from facenet_pytorch import InceptionResnetV1


class Siamese:
    def __init__(self):
        Siamese_network = InceptionResnetV1(pretrained='vggface2')
        checkpoint = torch.load("20180402-114759-vggface2.pt")
        Siamese_network.load_state_dict(checkpoint)
        Siamese_network = Siamese_network.cuda()
        Siamese_network.eval()
        self.Siamese_network = Siamese_network
        self.cos = nn.CosineSimilarity(dim=1, eps=1e-6)
        self.team_embedding = torch.load("team_embedding.pth")

    def face_recognition(self, detected_face, names):

        for det_face in detected_face[0]:
            similarity_list = []
            # embedding_list = []
            embedding1 = self.Siamese_network(det_face.permute(2, 0, 1).unsqueeze(0))
            for index, name in enumerate(names):
                # embedding2 = self.Siamese_network(temp[1])
                # embedding_list.append(embedding2)
                cosine_similarity = self.cos(embedding1, self.team_embedding[index]).item()
                similarity_list.append({name: cosine_similarity})
            # torch.save(embedding_list, '/home/timo/face_recognition/team_images/team_embedding.pth')
            detected_face.append(similarity_list)
        return detected_face

