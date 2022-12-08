function kilosort2_5_master(fpath, kilosortPath)
    try
        set(groot,'defaultFigureVisible', 'off');
        % https://github.com/MouseLand/Kilosort/issues/199#issuecomment-754971599
        disp('Setting latest mkl version');
        setenv('BLAS_VERSION', '/usr/lib/x86_64-linux-gnu/mkl/libblas.so');
        setenv('LAPACK_VERSION', '/usr/lib/x86_64-linux-gnu/mkl/liblapack.so');
        version -blas;
        version -lapack;

        if ~isdeployed
            % prepare for kilosort execution
            addpath(genpath(kilosortPath));

            % add npy-matlab functions (copied in the output folder)
            addpath(genpath(fpath));
        end

        % Load channel map file
        load(fullfile(fpath, 'chanMap.mat'));

        % Load the configuration file, it builds the structure of options (ops)
        load(fullfile(fpath, 'ops.mat'));

        % NEW STEP TO DO DATA REGISTRATION
        if isfield(ops, 'do_preprocessing')
            do_preprocessing = ops.do_preprocessing 
        else
            do_preprocessing = 1;
        end
        
        if do_preprocessing
            fprintf("Preprocessing/bin file copy ENABLED\n");
        else
            fprintf("Preprocessing/bin file copy DISABLED\n");
        end

        % preprocess data to create temp_wh.dat
        rez = preprocessDataSub(ops);

        % NEW STEP TO DO DATA REGISTRATION
        if isfield(ops, 'do_correction')
            do_correction = ops.do_correction;
        else
            do_correction = 1;
        end

        if do_correction
            fprintf("Drift correction ENABLED\n");
        else
            fprintf("Drift correction DISABLED\n");
        end

        rez = datashift2(rez, do_correction); % last input is for shifting data

        % ORDER OF BATCHES IS NOW RANDOM, controlled by random number generator
        iseed = 1;

        % main tracking and template matching algorithm
        rez = learnAndSolve8b(rez, iseed);

        % OPTIONAL: remove double-counted spikes - solves issue in which individual spikes are assigned to multiple templates.
        % See issue 29: https://github.com/MouseLand/Kilosort/issues/29
        rez = remove_ks2_duplicate_spikes(rez, "overlap_s", 0.0001);

        % final merges
        rez = find_merges(rez, 1);

        % final splits by SVD
        rez = splitAllClusters(rez, 1);

        % decide on cutoff
        rez = set_cutoff(rez);
        % eliminate widely spread waveforms (likely noise)
        rez.good = get_good_units(rez);

        fprintf('found %d good units \n', sum(rez.good>0))

        % write to Phy
        fprintf('Saving results to Phy  \n')
        rezToPhy(rez, fullfile(fpath));
    catch
        fprintf('----------------------------------------');
        fprintf(lasterr());
        quit(1);
    end
    quit(0);
end
