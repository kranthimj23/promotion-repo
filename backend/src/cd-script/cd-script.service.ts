import { Injectable, Logger, NotFoundException } from '@nestjs/common';
import { exec } from 'child_process';
import { promisify } from 'util';
import * as path from 'path';
import { PrismaService } from '../prisma/prisma.service';

const execPromise = promisify(exec);

@Injectable()
export class CDScriptService {
    private readonly logger = new Logger(CDScriptService.name);
    private readonly pythonPath = 'D:\\GarudaBE\\BE_unified_state\\backend\\.venv\\Scripts\\python.exe';
    private readonly garudaBePath = 'D:\\GarudaBE\\BE_unified_state\\backend\\app\\cd\\scripts';

    constructor(private readonly prisma: PrismaService) { }

    private getEnv() {
        const env = { ...process.env };
        env.PYTHONPATH = this.garudaBePath + (env.PYTHONPATH ? path.delimiter + env.PYTHONPATH : '');
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
            where: { projectId: params.projectId }
        });

        if (!promoRepo) {
            throw new NotFoundException(`Promotion repository for project "${params.projectId}" not found`);
        }

        const scriptPath = path.join(this.garudaBePath, 'create_release_note.py');
        const command = `${this.pythonPath} "${scriptPath}" "${params.sourceBranch}" "${params.destinationBranch}" "${params.lowerEnv}" "${params.higherEnv}" "${promoRepo.repoUrl}"`;

        this.logger.log(`Executing: ${command}`);
        try {
            const { stdout, stderr } = await execPromise(command, { env: this.getEnv(), cwd: this.garudaBePath });
            if (stderr) this.logger.warn(`Script stderr: ${stderr}`);
            return { success: true, output: stdout };
        } catch (error) {
            this.logger.error(`Script execution failed: ${error.message}`);
            return { success: false, error: error.message, output: error.stdout };
        }
    }

    async executeGenerateConfig(params: {
        projectId: string;
        environment: string;
        releaseBranch: string;
    }) {
        const scriptPath = path.join(this.garudaBePath, 'generate-config.py');
        const command = `${this.pythonPath} "${scriptPath}" --env "${params.environment}" --branch "${params.releaseBranch}" --project "${params.projectId}"`;

        this.logger.log(`Executing: ${command}`);
        try {
            const { stdout, stderr } = await execPromise(command, { env: this.getEnv(), cwd: this.garudaBePath });
            if (stderr) this.logger.warn(`Script stderr: ${stderr}`);
            return { success: true, output: stdout };
        } catch (error) {
            this.logger.error(`Script execution failed: ${error.message}`);
            return { success: false, error: error.message, output: error.stdout };
        }
    }

    async executeDeploy(params: {
        projectId: string;
        type: string;
    }) {
        const promoRepo = await this.prisma.promotionRepo.findUnique({
            where: { projectId: params.projectId }
        });

        if (!promoRepo) {
            throw new NotFoundException(`Promotion repository for project "${params.projectId}" not found`);
        }

        const scriptPath = path.join(this.garudaBePath, 'deploy.py');
        // deploy.py expects: <env> <repo_url> <branch>
        const command = `${this.pythonPath} "${scriptPath}" "dev1" "${promoRepo.repoUrl}" "master" --type "${params.type}" --project "${params.projectId}"`;

        this.logger.log(`Executing: ${command}`);
        try {
            const { stdout, stderr } = await execPromise(command, { env: this.getEnv(), cwd: this.garudaBePath });
            if (stderr) this.logger.warn(`Script stderr: ${stderr}`);
            return { success: true, output: stdout };
        } catch (error) {
            this.logger.error(`Script execution failed: ${error.message}`);
            return { success: false, error: error.message, output: error.stdout };
        }
    }
}
