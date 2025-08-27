num_partitions = 2; % You can increase this for more intervals
%define an array of optimal responses for R in CS
receiver_response_CS = zeros(1, num_partitions);
%define an array of optimal responses for R under ambiguity
receiver_response_ambi = zeros(1, num_partitions);

% Define parameters (ensure these are defined)
bias = 0.05;
max_iterations = 1000;
tolerance = 1e-6;

%define beta
beta = 0.01;
%beta = 1.5;


%distribution g_1(theta) = 2*theta
g_1 = @(theta) 2*theta;

%R's strategy in CS
function root_CS = receiver_optimal_CS(y1, y2, g_1)
    denominator = integral(@(theta) g_1(theta), y1, y2);
    root_CS = (integral(@(theta) theta.*g_1(theta), y1, y2))/denominator;

end

%R's strategy under ambiguity
function root_ambiguity = receiver_optimal_ambiguity(y1, y2, g_1,beta_parameter)
    F_ambiguity = @(a) integral(@(theta) (theta -a).*exp(((theta - a).^2) / beta_parameter).*g_1(theta), y1, y2);
    rootFunction = @(a) F_ambiguity(a);
    root_ambiguity = fzero(rootFunction,(y1+y2)/2);
end

%R's strategy under ambiguity
% function root_ambiguity = receiver_optimal_ambi(y1, y2,initial,beta_parameter)
%     F_normal = @(a) integral(@(theta) (theta -a).*exp(((theta - a).^2) / beta_parameter).*g_1(theta), y1, y2);
%     rootFunction = @(a) F_normal(a);
%     root_ambiguity = fzero(rootFunction, initial);
% end

%plot CS cut-offs
[eqm_CS_cutoff,receiver_response_CS] = find_eqm_CS(num_partitions,bias,max_iterations,tolerance,g_1);

%plot ambiguity cut-offs
[eqm_ambi_cutoff,receiver_response_ambi] = find_eqm_ambi(num_partitions,bias,max_iterations,tolerance,g_1,beta);

function [eqm_CS_cutoff,receiver_response_CS]  = find_eqm_CS(n,b,max_iter,tol,g_1)

    % Initialize variables to store the results
    partition_boundaries = linspace(0, 1, n + 1);
    equilibrium_partitions = partition_boundaries;
    converged = false;
    iteration = 0;
    while ~converged && iteration < max_iter
        iteration = iteration + 1;
        old_partitions = equilibrium_partitions;
        % Step 1: Receiver's optimal action
        y_star = zeros(1, n);
        for i = 1:n
            m_lower = partition_boundaries(i);
            m_upper = partition_boundaries(i+1);
            % Receiver's optimal action is the expected value of the partition
            y_star(i) = receiver_optimal_CS(m_lower,m_upper,g_1);
            receiver_response_CS(i) = y_star(i); % Store the optimal action
        end
        
        % Step 2: Sender's strategy and new partitions
        for i = 2:n
            % Update partition boundaries by finding the point where the sender is indifferent
            equilibrium_partitions(i) = (y_star(i-1) + y_star(i)) / 2 - b;
        end
        
        % Check for convergence
        if max(abs(equilibrium_partitions - old_partitions)) < tol
            converged = true;
        end
        partition_boundaries = equilibrium_partitions;
    end
    
    % Display results
    disp('Equilibrium partition boundaries for g_1 distribution in CS:')
    disp(equilibrium_partitions)
    disp('Receiver optimal responses:');
    disp(receiver_response_CS); % Display the stored responses
    eqm_CS_cutoff = equilibrium_partitions;
end


function [eqm_ambi_cutoff,receiver_response_ambi] = find_eqm_ambi(n,b,max_iter,tol,g_1,beta_parameter)
    
    % Initialize variables to store the results
    partition_boundaries = linspace(0, 1, n + 1);
    equilibrium_partitions = partition_boundaries;
    converged = false;
    iteration = 0;
    while ~converged && iteration < max_iter
        iteration = iteration + 1;
        old_partitions = equilibrium_partitions;
        % Step 1: Receiver's optimal action
        y_star = zeros(1, n);
        for i = 1:n
            m_lower = partition_boundaries(i);
            m_upper = partition_boundaries(i+1);
            % Receiver's optimal action is the expected value of the partition
            y_star(i) = receiver_optimal_ambiguity(m_lower,m_upper,g_1,beta_parameter);
            receiver_response_ambi(i) = y_star(i); % Store the optimal action
        end
        
        % Step 2: Sender's strategy and new partitions
        for i = 2:n
            % Update partition boundaries by finding the point where the sender is indifferent
            equilibrium_partitions(i) = (y_star(i-1) + y_star(i)) / 2 - b;
        end
        
        % Check for convergence
        if max(abs(equilibrium_partitions - old_partitions)) < tol
            converged = true;
        end
        partition_boundaries = equilibrium_partitions;
    end

    % Display results
    disp('Equilibrium partition boundaries for g_1 distribution under ambiguity:')
    disp(equilibrium_partitions)
    disp('Receiver optimal responses under ambiguity:');
    disp(receiver_response_ambi); % Display the stored responses
    eqm_ambi_cutoff = equilibrium_partitions;
end

% Plot the segment [0, 1] with partition boundaries
figure;
hold on;
xlim([0 1]);
ylim([-0.2 0.2]);

% Plot the line representing the segment [0, 1]
h1 = plot([0 1], [0 0], 'k-', 'LineWidth', 2); % h1 is the handle for the Segment

% Plot the partition boundaries of CS (Red lines)
for i = 1:length(eqm_CS_cutoff)
    x = eqm_CS_cutoff(i);
    h2 = plot([x x], [-0.05 0.05], 'r-', 'LineWidth', 2); % h2 is the handle for CS Boundaries
    text(x, 0.06, sprintf('%.2f', x), 'HorizontalAlignment', 'center', 'FontSize', 15, 'Color', 'r');
end

% Plot R's best responses in CS (Blue lines)
for i = 1:length(receiver_response_CS)
    y = receiver_response_CS(i);
    h3 = plot([y y], [-0.05 0.05], 'b-', 'LineWidth', 2); % h3 is the handle for CS Responses
    text(y, 0.06, sprintf('%.2f', y), 'HorizontalAlignment', 'center', 'FontSize', 15, 'Color', 'b');
end

% Plot the partition boundaries under ambiguity (Red dashed lines)
for i = 1:length(eqm_ambi_cutoff)
    x_ambi = eqm_ambi_cutoff(i);
    h4 = plot([x_ambi x_ambi], [-0.1 -0.02], 'r--', 'LineWidth', 2); % h4 is the handle for Ambiguity Boundaries
    text(x_ambi, -0.11, sprintf('%.2f', x_ambi), 'HorizontalAlignment', 'center', 'FontSize', 15, 'Color', 'r');
end

% Plot R's best responses under ambiguity (Blue dashed lines)
for i = 1:length(receiver_response_ambi)
    y_ambi = receiver_response_ambi(i);
    h5 = plot([y_ambi y_ambi], [-0.1 -0.02], 'b--', 'LineWidth', 2); % h5 is the handle for Ambiguity Responses
    text(y_ambi, -0.11, sprintf('%.2f', y_ambi), 'HorizontalAlignment', 'center', 'FontSize', 15, 'Color', 'b');
end

hold off;

% Add title and legend with specific plot handles
title(['Partition Boundaries and Receiver Responses: CS vs. Ambiguity with N =', num2str(num_partitions), ', K = ', num2str(beta)], 'FontSize', 30);

% Use the plot handles to create a correctly ordered legend
legend([h1, h2, h3, h4, h5], 'Segment', 'CS Boundaries', 'CS Responses', 'CSUA Boundaries', 'CSUA Responses', 'FontSize', 15);

% Increase axis label and tick mark sizes
set(gca, 'FontSize', 12); % Adjust the font size for the axes (tick labels and axis labels)
