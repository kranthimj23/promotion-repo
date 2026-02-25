import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import { PrismaService } from '../prisma/prisma.service';

const execPromise = promisify(exec);

@Injectable()
export class CDScriptService {
    private readonly logger = new Logger(CDScriptService.name);
    private readonly pythonPath =
        'D:\\Garuda\\BE_unified_state\\backend\\.venv\\Scripts\\python.exe';
    private readonly garudaBePath =
        'D:\\Garuda\\BE_unified_state\\backend\\app\\cd\\scripts';
    private readonly servicesListPath =
        'D:\\Garuda\\BE_unified_state\\backend\\app\\cd\\services_list.txt';

    constructor(private readonly prisma: PrismaService) { }

    private getEnv() {
        const env: any = {
            ...process.env,
            ComSpec: process.env.ComSpec || 'C:\\Windows\\System32\\cmd.exe',
            SystemRoot: process.env.SystemRoot || 'C:\\Windows',
            PYTHONIOENCODING: 'utf-8',
            GIT_TOKEN: process.env.GIT_TOKEN
        };
        env.PYTHONPATH =
            this.garudaBePath +
            (env.PYTHONPATH ? path.delimiter + env.PYTHONPATH : '');
        return env;
    }

    async executeCreateReleaseNote(params: {
        projectId: string;
        lowerEnv: string;
        higherEnv: string;
        sourceBranch: string;
        destinationBranch: string;
    }) {
        const promoRepo = await this.prisma.promotionRepo.findUnique({
            where: { projectId: params.projectId },
        });

        if (!promoRepo) {
            throw new NotFoundException(
                `Promotion repository for project "${params.projectId}" not found`,
            );
        }

        // Extract version from destinationBranch (e.g., "release/1.0.0" -> "1.0.0")
        const newVersion = params.destinationBranch.replace('release/', '');

        const scriptPath = path.join(this.garudaBePath, 'main.py');
        const command = `"${this.pythonPath}" "${scriptPath}" "${params.lowerEnv}" "${params.higherEnv}" "${promoRepo.repoUrl}" "${newVersion}" "${this.servicesListPath}" "${params.sourceBranch}"`;

        this.logger.log(`Executing Pipeline Orchestrator: ${command}`);
        try {
            const { stdout, stderr } = await execPromise(command, {
                env: this.getEnv(),
                cwd: this.garudaBePath,
            });
            if (stderr) this.logger.warn(`Script stderr: ${stderr}`);
            return { success: true, output: stdout };
        } catch (error) {
            this.logger.error(`Pipeline execution failed: ${error.message}`);
            return { success: false, error: error.message, output: error.stdout };
        }
    }

    async executeGenerateConfig(params: {
        projectId: string;
        environment: string;
        releaseBranch: string;
    }) {
        const promoRepo = await this.prisma.promotionRepo.findUnique({
            where: { projectId: params.projectId },
        });

        if (!promoRepo) {
            throw new NotFoundException(
                `Promotion repository for project "${params.projectId}" not found`,
            );
        }

        // Get the target environment (higher_env)
        const higherEnv = await this.prisma.environment.findUnique({
            where: {
                projectId_name: {
                    projectId: params.projectId,
                    name: params.environment,
                },
            },
        });

        if (!higherEnv) {
            throw new NotFoundException(`Environment "${params.environment}" not found`);
        }

        // Determine lower_env (previous in promotion order)
        let lowerEnvName = 'dev'; // Default fallback
        if (higherEnv.promotionOrder > 1) {
            const lowerEnv = await this.prisma.environment.findFirst({
                where: {
                    projectId: params.projectId,
                    promotionOrder: higherEnv.promotionOrder - 1,
                },
            });
            if (lowerEnv) {
                lowerEnvName = lowerEnv.name;
            }
        }

        // Fetch previous stable branch (the one before the current target branch)
        const previousBranchRecord = await this.prisma.branchTracker.findFirst({
            where: {
                projectId: params.projectId,
                branchName: {
                    not: params.releaseBranch
                }
            },
            orderBy: {
                createdAt: 'desc'
            }
        });

        const previousBranch = previousBranchRecord?.branchName || 'release/8.0.10';

        const scriptPath = path.join(this.garudaBePath, 'generate-config.py');

        // generate-config.py expects: <prev_branch> <target_branch> <lower_env> <higher_env> <repo_url>
        const command = `"${this.pythonPath}" "${scriptPath}" "${previousBranch}" "${params.releaseBranch}" "${lowerEnvName}" "${params.environment}" "${promoRepo.repoUrl}"`;

        this.logger.log(`Executing: ${command}`);
        try {
            const { stdout, stderr } = await execPromise(command, {
                env: this.getEnv(),
                cwd: this.garudaBePath,
            });
            if (stderr) this.logger.warn(`Script stderr: ${stderr}`);
            return { success: true, output: stdout };
        } catch (error) {
            this.logger.error(`Script execution failed: ${error.message}`);
            return { success: false, error: error.message, output: error.stdout };
        }
    }

    async executeDeploy(params: { projectId: string; type: string }) {
        const promoRepo = await this.prisma.promotionRepo.findUnique({
            where: { projectId: params.projectId },
        });

        if (!promoRepo) {
            throw new NotFoundException(
                `Promotion repository for project "${params.projectId}" not found`,
            );
        }

        const scriptPath = path.join(this.garudaBePath, 'deploy.py');
        // deploy.py expects: <env> <repo_url> <branch>
        const command = `${this.pythonPath} "${scriptPath}" "dev1" "${promoRepo.repoUrl}" "master" --type "${params.type}" --project "${params.projectId}"`;

        this.logger.log(`Executing: ${command}`);
        try {
            const { stdout, stderr } = await execPromise(command, {
                env: this.getEnv(),
                cwd: this.garudaBePath,
            });
            if (stderr) this.logger.warn(`Script stderr: ${stderr}`);
            return { success: true, output: stdout };
        } catch (error) {
            this.logger.error(`Script execution failed: ${error.message}`);
            return { success: false, error: error.message, output: error.stdout };
        }
    }
}
