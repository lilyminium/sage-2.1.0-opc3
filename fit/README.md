# Fitting

## optimize.in

This is the config file for ForceBalance.
As no options were changed for this fit from Sage 2.0,
this was downloaded from the openff-sage repo.

```
curl -O https://raw.githubusercontent.com/openforcefield/openff-sage/main/inputs-and-results/optimizations/vdw-v1/optimize.in
```

## Training data

As this was not changed from the Sage 2.0 fit,
it was downloaded from the openff-sage repo.

```
mkdir -p targets/phys-prop
curl https://raw.githubusercontent.com/openforcefield/openff-sage/main/inputs-and-results/optimizations/vdw-v1/targets/phys-prop/training-set.json --output targets/phys-prop/training-set.json
```

## Setting up options

