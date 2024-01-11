import torch
import numpy, tqdm
from .Audio_Tools import Audio


ForbeniousNorm = lambda A, B: 1-(torch.abs(torch.linalg.norm(A.squeeze(0), ord="fro")-torch.linalg.norm(B.squeeze(0), ord="fro"))/2)

Correct = lambda Source, Target: Target.eq(Source).sum().item()



def EqualErrorRate(forward_fn: torch.nn.Module,
                   evaluation_pair_list:list,
                   device:torch.device,
                   similarity:str="cosine",
                   simlarity_dim:int=0,
                   p_target:float=0.05,
                   c_miss:float=1.0,
                   c_fa:float=1.0,
                   *args, **kwargs):

    if similarity not in ["cosine", "forbenious"]:
        raise Exception(f"Not yet implemented for {similarity}")
    
    if similarity == "cosine":
        Similarity = torch.nn.CosineSimilarity(dim=simlarity_dim)
    if similarity == "forbenious":
        Similarity = ForbeniousNorm
    
    scores, labels = [], []
    
    with torch.no_grad():
        for i in tqdm.tqdm(evaluation_pair_list, 
                           desc=" EER pairs",
                        #    position=2,
                           colour="magenta",
                           leave=False):
            aud_1, _ = Audio().load(path=i["path_1"], audio_duration="full", audio_normalization=True)
            aud_2, _ = Audio().load(path=i["path_2"], audio_duration="full", audio_normalization=True)
            
            try:
                emb_1 = forward_fn(aud_1.to(device))
                emb_2 = forward_fn(aud_2.to(device))
            except Exception as _:
                emb_1 = forward_fn(aud_1.unsqueeze(0).to(device)).squeeze(0)
                emb_2 = forward_fn(aud_2.unsqueeze(0).to(device)).squeeze(0)
            
            scores.append(Similarity(emb_1, emb_2).item())      
            
            if type(i["match"]) == str:
                labels.append(int(i["match"]))
            if type(i["match"]) == int:
                labels.append(i["match"])     
                
    label_set = list(numpy.unique(labels))

    assert len(label_set) == 2, f'the input labels must contains both two labels, but recieved set(labels) = {label_set}'

    label_set.sort()
    assert label_set == [0, 1], 'the input labels must contain 0 and 1 for distinct and identical id. '

    same_id_scores = scores[labels == 1]
    diff_id_scores = scores[labels == 0]
    thresh = numpy.linspace(numpy.min(diff_id_scores), numpy.max(same_id_scores), 1000)
    thresh = numpy.expand_dims(thresh, 1)
    fr_matrix = same_id_scores < thresh
    fa_matrix = diff_id_scores >= thresh
    fr_rate = numpy.mean(fr_matrix, 1)
    fa_rate = numpy.mean(fa_matrix, 1)

    thresh_idx = numpy.argmin(numpy.abs(fa_rate - fr_rate))
    eer = (fr_rate[thresh_idx] + fa_rate[thresh_idx]) / 2
    thresh = thresh[thresh_idx, 0]
        
    dcf = c_miss * fr_rate * p_target + c_fa * fa_rate * (1 - p_target)
    c_det = numpy.min(dcf)
    c_def = min(c_miss * p_target, c_fa * (1 - p_target))
    min_cdf = c_det / c_def
        
    return eer*100, min_cdf
