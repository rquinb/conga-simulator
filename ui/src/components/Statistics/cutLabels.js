function getLabels(playerCuts){
    return playerCuts.map((value)=> value == "no_cut" ? "Sin corte" : value == "normal_cut" ? "Corte normal" : value == "zero_cut" ? "Corte en Cero" : "Conga")
}

export {getLabels}