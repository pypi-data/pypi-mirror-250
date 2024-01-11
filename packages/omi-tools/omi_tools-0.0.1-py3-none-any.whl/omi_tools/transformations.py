import pywt
import numpy as np
from symfit import Fit


def ft(array, model_dict):
    period_mul = array.shape[1] // 720
    xdata = np.array([np.linspace(-2 * np.pi, 2 * period_mul * np.pi, array.shape[1]) for _ in range(array.shape[0])])
    fit = Fit(model_dict, x=xdata, y=array)
    fit_result = fit.execute()
    y_fourier = fit_result.params

    return y_fourier.values(), fit.model(x=xdata, **fit_result.params).y


def inverse_ft(params, shape):
    xdata = np.array([np.linspace(-2 * np.pi, 2 * np.pi, shape[1]) for _ in range(shape[0])])
    sigma = np.full((shape[0], shape[1]), params["a0"])
    for k in range(1, len(params) // 2 - 1):
        sigma += params[f"a{k}"] * np.cos(k * params["w"] * xdata)
        sigma += params[f"b{k}"] * np.sin(k * params["w"] * xdata)

    return sigma.T


def get_ft_param_names(model_dict):
    xdata = np.linspace(-2 * np.pi, 2 * np.pi, 10)
    fit = Fit(model_dict, x=xdata, y=xdata)
    fit_result = fit.execute()

    return list(fit_result.params.keys())


def dwt(array, level, wavelet):
    decomposition = pywt.wavedec(array, wavelet, mode="per", level=level)
    y_wavelet = decomposition[0]
    decomposition[1:len(decomposition)] = [np.zeros_like(decomposition[d]) for d in
                                           range(1, len(decomposition))]

    return y_wavelet, pywt.waverec(decomposition, wavelet, mode="per")


def inverse_dwt(c, level, wavelet):
    decomposition = []
    curr_len = len(c)
    decomposition.append(c)
    for l in range(1, level + 1):
        decomposition.append(np.zeros(curr_len))
        curr_len *= 2

    return pywt.waverec(decomposition, wavelet, mode="per")


def denoise(array, level, wavelet, threshold=0.33):
    decomposition = pywt.wavedec(data=array, wavelet=wavelet, mode="per", level=level)
    for k in range(len(decomposition)):
        decomposition[k] = pywt.threshold(decomposition[k], threshold, mode="hard")
    y_denoise = pywt.waverec(decomposition, wavelet, mode="per")

    return y_denoise, y_denoise
